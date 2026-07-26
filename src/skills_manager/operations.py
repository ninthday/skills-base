import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from shutil import Error, copy2, copytree, move, rmtree
from subprocess import CalledProcessError

import questionary

from .git import run_git
from .models import Metadata


@dataclass(frozen=True)
class Project:
    name: str
    source: str
    type: str
    path: Path


def projects_from_metadata(metadata: Metadata) -> tuple[Project, ...]:
    sources = tuple(
        Project(name, source, "source", Path("sources") / name)
        for name, source in metadata.submodules.items()
    )
    vendors = tuple(
        Project(name, vendor.source, "vendor", Path("vendor") / name)
        for name, vendor in metadata.vendors.items()
    )
    return (*sources, *vendors)


def expected_skill_names(metadata: Metadata) -> set[str]:
    return {
        *metadata.submodules,
        *(
            output
            for vendor in metadata.vendors.values()
            for output in vendor.skills.values()
        ),
        *metadata.manual,
    }


def existing_submodule_paths(root: Path) -> set[Path]:
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return set()

    output = run_git(
        ["config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$"],
        root,
        check=False,
    )
    paths: set[Path] = set()
    for line in output.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            paths.add(Path(parts[1]))
    return paths


def remove_submodule(root: Path, path: Path) -> None:
    run_git(["submodule", "deinit", "-f", str(path)], root, check=False)
    modules_path = root / ".git" / "modules" / path
    if modules_path.exists():
        rmtree(modules_path)
    run_git(["rm", "-f", str(path)], root)


def _confirm_removal(message: str, assume_yes: bool) -> bool | None:
    if assume_yes:
        return True
    return questionary.confirm(message, default=True).ask()


def _remove_extra_submodules(
    root: Path, metadata: Metadata, assume_yes: bool
) -> tuple[bool, bool]:
    expected_paths = {project.path for project in projects_from_metadata(metadata)}
    extra_paths = sorted(existing_submodule_paths(root) - expected_paths)
    if not extra_paths:
        return False, True

    print(f"Found {len(extra_paths)} submodule(s) not in meta.py:")
    for path in extra_paths:
        print(f"  - {path}")

    should_remove = _confirm_removal("Remove these extra submodules?", assume_yes)
    if should_remove is None:
        print("Cancelled")
        return False, False
    if not should_remove:
        return False, True

    for path in extra_paths:
        try:
            remove_submodule(root, path)
            print(f"Removed: {path}")
        except CalledProcessError as error:
            print(f"Failed to remove {path}: {error}")
    return True, True


def init_submodules(root: Path, metadata: Metadata, assume_yes: bool) -> int:
    try:
        run_git(
            [
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--init",
                "--recursive",
            ],
            root,
        )
    except CalledProcessError as error:
        print(f"Failed to initialize existing submodules: {error}")
        return 1

    _, should_continue = _remove_extra_submodules(root, metadata, assume_yes)
    if not should_continue:
        return 0

    existing_paths = existing_submodule_paths(root)
    new_projects = [
        project
        for project in projects_from_metadata(metadata)
        if project.path not in existing_paths
    ]
    existing_projects = [
        project
        for project in projects_from_metadata(metadata)
        if project.path in existing_paths
    ]
    if not new_projects:
        print("All submodules already initialized")
        return 0

    if assume_yes:
        selected = new_projects
    else:
        selected = questionary.checkbox(
            "Select projects to initialize",
            choices=[
                questionary.Choice(
                    title=f"{project.name} ({project.type})",
                    value=project,
                    checked=True,
                )
                for project in new_projects
            ],
        ).ask()
        if selected is None:
            print("Cancelled")
            return 0

    for project in selected:
        (root / project.path).parent.mkdir(parents=True, exist_ok=True)
        try:
            run_git(
                [
                    "-c",
                    "protocol.file.allow=always",
                    "submodule",
                    "add",
                    project.source,
                    str(project.path),
                ],
                root,
            )
            print(f"Added: {project.name}")
        except CalledProcessError as error:
            print(f"Failed to add {project.name}: {error}")

    print("Submodules initialized")
    if existing_projects:
        print(
            f"Already initialized: {', '.join(project.name for project in existing_projects)}"
        )
    return 0


def _copy_license(vendor_path: Path, output_path: Path) -> None:
    for name in (
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
        "license",
        "license.md",
        "license.txt",
    ):
        license_path = vendor_path / name
        if license_path.is_file():
            copy2(license_path, output_path / "LICENSE.md")
            return


def _vendor_sha(vendor_path: Path) -> str | None:
    try:
        return run_git(["rev-parse", "HEAD"], vendor_path)
    except CalledProcessError:
        return None


def _upstream_skill_exists(vendor_path: Path, source_name: str) -> bool | None:
    try:
        output = run_git(
            ["ls-tree", "-d", "--name-only", "@{u}", "--", f"skills/{source_name}"],
            vendor_path,
        )
    except CalledProcessError:
        return None
    return bool(output)


def _record_upstream_removal(output_path: Path) -> str | None:
    sync_info_path = output_path / "SYNC.md"
    try:
        sync_info = (
            sync_info_path.read_text(encoding="utf-8")
            if sync_info_path.exists()
            else "# Sync Info\n"
        )
    except OSError as error:
        print(f"Failed to read sync info for {output_path.name}: {error}")
        return None

    prefix = "- **Upstream Removed:** "
    for line in sync_info.splitlines():
        if line.startswith(prefix):
            return line.removeprefix(prefix)

    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    try:
        sync_info_path.write_text(
            f"{sync_info.rstrip()}\n{prefix}{timestamp}\n", encoding="utf-8"
        )
    except OSError as error:
        print(f"Failed to record upstream removal for {output_path.name}: {error}")
        return None
    return timestamp


def _archive_invalid_vendor_skill(root: Path, output_name: str) -> None:
    output_path = root / "skills" / output_name
    archive_root = root / "archived-skills" / output_name
    if not output_path.exists():
        if archive_root.is_dir():
            print(f"Already archived invalid vendor skill: {output_name}")
        else:
            print(f"Invalid vendor skill has no local output: {output_name}")
        return

    timestamp = _record_upstream_removal(output_path)
    if timestamp is None:
        return

    destination = archive_root / timestamp
    suffix = 2
    while destination.exists():
        destination = archive_root / f"{timestamp}-{suffix}"
        suffix += 1
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        move(str(output_path), str(destination))
    except (Error, OSError) as error:
        print(f"Failed to archive invalid vendor skill {output_name}: {error}")
        return
    print(
        f"Archived invalid vendor skill: {output_name} → "
        f"{destination.relative_to(root)}"
    )


def sync_submodules(root: Path, metadata: Metadata) -> int:
    try:
        run_git(
            [
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--remote",
                "--merge",
            ],
            root,
        )
    except CalledProcessError as error:
        print(f"Failed to update submodules: {error}")
        return 1

    invalid_skills: list[tuple[str, str]] = []
    for vendor_name, vendor in metadata.vendors.items():
        vendor_path = root / "vendor" / vendor_name
        vendor_skills = vendor_path / "skills"
        if not vendor_path.is_dir():
            print(f"Vendor submodule not found: {vendor_name}. Run init first.")
            continue
        if not vendor_skills.is_dir():
            print(f"No skills directory in vendor/{vendor_name}/skills/")

        for source_name, output_name in vendor.skills.items():
            source_path = vendor_skills / source_name
            output_path = root / "skills" / output_name
            if not source_path.is_dir():
                invalid_skills.append(
                    (output_name, f"vendor/{vendor_name}/skills/{source_name}")
                )
                continue

            if output_path.exists():
                rmtree(output_path)
            copytree(source_path, output_path)
            _copy_license(vendor_path, output_path)
            sha = _vendor_sha(vendor_path)
            (output_path / "SYNC.md").write_text(
                "# Sync Info\n\n"
                f"- **Source:** `vendor/{vendor_name}/skills/{source_name}`\n"
                f"- **Git SHA:** `{sha}`\n"
                f"- **Synced:** {time.strftime('%Y-%m-%d')}\n",
                encoding="utf-8",
            )
            print(f"Synced: {source_name} → {output_name}")

    if invalid_skills:
        print("Invalid vendor skills:")
        for output_name, source_path in invalid_skills:
            print(f"- {output_name}: {source_path}")
            _archive_invalid_vendor_skill(root, output_name)

    print("All skills synced")
    return 0


def _behind_count(path: Path) -> int:
    try:
        output = run_git(["rev-list", "HEAD..@{u}", "--count"], path)
        return int(output)
    except (CalledProcessError, ValueError):
        return 0


def check_updates(root: Path, metadata: Metadata) -> int:
    try:
        run_git(
            ["submodule", "foreach", "git -c protocol.file.allow=always fetch"],
            root,
        )
    except CalledProcessError as error:
        print(f"Failed to fetch: {error}")
        return 1

    updates: list[tuple[str, str, int]] = []
    for project in projects_from_metadata(metadata):
        path = root / project.path
        if not path.is_dir():
            continue
        behind = _behind_count(path)
        if behind:
            name = project.name
            if project.type == "vendor":
                outputs = ", ".join(metadata.vendors[project.name].skills.values())
                name = f"{name} ({outputs})"
            updates.append((name, project.type, behind))

    invalid_skills: list[tuple[str, str]] = []
    for vendor_name, vendor in metadata.vendors.items():
        vendor_path = root / "vendor" / vendor_name
        if not vendor_path.is_dir():
            continue
        for source_name, output_name in vendor.skills.items():
            if _upstream_skill_exists(vendor_path, source_name) is False:
                invalid_skills.append(
                    (output_name, f"vendor/{vendor_name}/skills/{source_name}")
                )

    if updates:
        print("Updates available:")
        for name, project_type, behind in updates:
            print(f"  {name} ({project_type}): {behind} commits behind")
    else:
        print("All submodules are up to date")

    if invalid_skills:
        print("Invalid vendor skills:")
        for output_name, source_path in invalid_skills:
            print(f"- {output_name}: {source_path}")
    return 0


def _existing_skill_names(root: Path) -> Iterable[str]:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return ()
    return (entry.name for entry in skills_dir.iterdir() if entry.is_dir())


def cleanup(root: Path, metadata: Metadata, assume_yes: bool) -> int:
    changed, should_continue = _remove_extra_submodules(root, metadata, assume_yes)
    if not should_continue:
        return 0

    extra_skills = sorted(
        set(_existing_skill_names(root)) - expected_skill_names(metadata)
    )
    if extra_skills:
        print(f"Found {len(extra_skills)} skill(s) not in meta.py:")
        for name in extra_skills:
            print(f"  - skills/{name}")

        should_remove = _confirm_removal("Remove these extra skills?", assume_yes)
        if should_remove is None:
            print("Cancelled")
            return 0
        if should_remove:
            changed = True
            for name in extra_skills:
                try:
                    rmtree(root / "skills" / name)
                    print(f"Removed: skills/{name}")
                except OSError as error:
                    print(f"Failed to remove skills/{name}: {error}")

    if changed:
        print("Cleanup completed")
    elif not extra_skills:
        print("Everything is clean, no unused submodules or skills found")
    return 0

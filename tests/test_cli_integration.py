from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]


def git(path: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=path,
        check=True,
        capture_output=True,
        encoding="utf-8",
        text=True,
    )
    return completed.stdout.strip()


def create_repository(path: Path, files: dict[str, str]) -> Path:
    path.mkdir()
    git(path, "init", "--initial-branch=main")
    git(path, "config", "user.name", "Test User")
    git(path, "config", "user.email", "test@example.com")
    for relative_path, content in files.items():
        destination = path / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    git(path, "add", ".")
    git(path, "commit", "--allow-empty", "-m", "Initial commit")
    return path


def write_metadata(root: Path, vendor_source: Path) -> None:
    (root / "pyproject.toml").write_text(
        "[project]\nname = 'fixture-project'\nversion = '0'\nrequires-python = '>=3.13'\n",
        encoding="utf-8",
    )
    (root / "meta.py").write_text(
        "from skills_manager.models import VendorSkillMeta\n\n"
        "submodules = {}\n"
        "vendors = {\n"
        f"    'example': VendorSkillMeta(source={str(vendor_source)!r}, "
        "skills={'engineering/example': 'example-skill'}),\n"
        "}\n"
        "manual = ('manual-skill',)\n",
        encoding="utf-8",
    )


def run_cli(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ | {"PYTHONPATH": str(PROJECT_ROOT / "src")}
    return subprocess.run(
        [sys.executable, "-m", "skills_manager.cli", *args],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        encoding="utf-8",
        text=True,
    )


def add_submodule(root: Path, source: Path, path: str) -> None:
    git(root, "-c", "protocol.file.allow=always", "submodule", "add", str(source), path)


def test_cli_manages_local_submodules_and_skills(tmp_path: Path) -> None:
    vendor_source = create_repository(
        tmp_path / "vendor-source",
        {
            "LICENSE": "Example license\n",
            "skills/engineering/example/SKILL.md": "# Example skill\n",
        },
    )
    extra_source = create_repository(
        tmp_path / "extra-source", {"README.md": "extra\n"}
    )
    root = create_repository(tmp_path / "project", {})
    write_metadata(root, vendor_source)
    git(root, "add", "meta.py", "pyproject.toml")
    git(root, "commit", "-m", "Add fixture metadata")
    add_submodule(root, extra_source, "vendor/extra")

    initialized = run_cli(root, "init", "--yes")
    assert initialized.returncode == 0, initialized.stderr
    assert (root / "vendor" / "example" / "skills").is_dir()
    assert not (root / "vendor" / "extra").exists()

    synchronized = run_cli(root, "sync")
    assert synchronized.returncode == 0, synchronized.stderr
    output = root / "skills" / "example-skill"
    assert (output / "SKILL.md").read_text(encoding="utf-8") == "# Example skill\n"
    assert (output / "LICENSE.md").read_text(encoding="utf-8") == "Example license\n"
    vendor_sha = git(root / "vendor" / "example", "rev-parse", "HEAD")
    sync_info = (output / "SYNC.md").read_text(encoding="utf-8")
    assert "- **Source:** `vendor/example/skills/engineering/example`" in sync_info
    assert f"- **Git SHA:** `{vendor_sha}`" in sync_info

    checked = run_cli(root, "check")
    assert checked.returncode == 0, checked.stderr
    assert "All submodules are up to date" in checked.stdout

    add_submodule(root, extra_source, "vendor/extra")
    (root / "skills" / "extra-skill").mkdir()
    cleaned = run_cli(root, "cleanup", "--yes")
    assert cleaned.returncode == 0, cleaned.stderr
    assert (root / "vendor" / "example").is_dir()
    assert not (root / "vendor" / "extra").exists()
    assert not (root / "skills" / "extra-skill").exists()


    source_skill = vendor_source / "skills" / "engineering" / "example" / "SKILL.md"
    source_skill.unlink()
    source_skill.parent.rmdir()
    git(vendor_source, "add", "--all")
    git(vendor_source, "commit", "-m", "Remove example skill")

    checked_after_removal = run_cli(root, "check")
    assert checked_after_removal.returncode == 0, checked_after_removal.stderr
    assert "Invalid vendor skills:" in checked_after_removal.stdout
    assert "example-skill" in checked_after_removal.stdout
    assert "vendor/example/skills/engineering/example" in checked_after_removal.stdout

    synchronized_after_removal = run_cli(root, "sync")
    assert synchronized_after_removal.returncode == 0, synchronized_after_removal.stderr
    assert "Archived invalid vendor skill: example-skill" in synchronized_after_removal.stdout
    assert not output.exists()

    archive_root = root / "archived-skills" / "example-skill"
    archived_paths = tuple(archive_root.iterdir())
    assert len(archived_paths) == 1
    archived_output = archived_paths[0]
    assert re.fullmatch(r"\d{8}T\d{6}Z", archived_output.name)
    assert (archived_output / "SKILL.md").read_text(encoding="utf-8") == "# Example skill\n"
    archived_sync_info = (archived_output / "SYNC.md").read_text(encoding="utf-8")
    assert "- **Source:** `vendor/example/skills/engineering/example`" in archived_sync_info
    assert f"- **Git SHA:** `{vendor_sha}`" in archived_sync_info
    assert (
        f"- **Upstream Removed:** {archived_output.name}" in archived_sync_info
    )
    assert archived_sync_info.count("- **Upstream Removed:**") == 1

    synchronized_again = run_cli(root, "sync")
    assert synchronized_again.returncode == 0, synchronized_again.stderr
    assert "Already archived invalid vendor skill: example-skill" in synchronized_again.stdout
    assert tuple(archive_root.iterdir()) == archived_paths

    checked_without_updates = run_cli(root, "check")
    assert checked_without_updates.returncode == 0, checked_without_updates.stderr
    assert "All submodules are up to date" in checked_without_updates.stdout
    assert "Invalid vendor skills:" in checked_without_updates.stdout

    cleaned_after_archive = run_cli(root, "cleanup", "--yes")
    assert cleaned_after_archive.returncode == 0, cleaned_after_archive.stderr
    assert archived_output.is_dir()

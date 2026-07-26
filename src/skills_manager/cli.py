import sys
from collections.abc import Sequence
from pathlib import Path

import questionary

from .metadata import MetadataError, discover_project_root, load_metadata
from .operations import check_updates, cleanup, init_submodules, sync_submodules

COMMANDS = ("init", "sync", "check", "cleanup")


def _choose_command() -> str | None:
    return questionary.select(
        "What would you like to do?",
        choices=[
            questionary.Choice("Sync submodules", "sync"),
            questionary.Choice("Init submodules", "init"),
            questionary.Choice("Check updates", "check"),
            questionary.Choice("Cleanup", "cleanup"),
        ],
    ).ask()


def main(argv: Sequence[str] | None = None) -> int:
    args = tuple(sys.argv[1:] if argv is None else argv)
    assume_yes = "-y" in args or "--yes" in args
    commands = [argument for argument in args if not argument.startswith("-")]
    command = commands[0] if commands else None

    if command is not None and command not in COMMANDS:
        print(f"Unknown command: {command}")
        return 1
    if command is None and assume_yes:
        print("Command required when using -y flag")
        return 1
    if command is None:
        command = _choose_command()
        if command is None:
            print("Cancelled")
            return 0

    try:
        root = discover_project_root(Path.cwd())
        metadata = load_metadata(root)
    except MetadataError as error:
        print(error)
        return 1

    if command == "init":
        return init_submodules(root, metadata, assume_yes)
    if command == "sync":
        return sync_submodules(root, metadata)
    if command == "check":
        return check_updates(root, metadata)
    return cleanup(root, metadata, assume_yes)


if __name__ == "__main__":
    raise SystemExit(main())

import subprocess
from collections.abc import Sequence
from pathlib import Path


def run_git(args: Sequence[str], cwd: Path, *, check: bool = True) -> str:
    """Run Git without shell interpolation and return its standard output."""
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
    )
    return completed.stdout.strip()

from __future__ import annotations

from pathlib import Path

ROOT_PATH = Path(__file__).parent


def get_respath(*parts: str | Path) -> str:
    """Get the absolute path to a resource (POSIX format).

    Args:
        *parts: Path components relative to the package root.

    Returns:
        str: The absolute POSIX path to the resource.
    """
    return (ROOT_PATH / Path(*parts)).as_posix()

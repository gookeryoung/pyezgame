from pathlib import Path
from typing import Union

ROOT_PATH = Path(__file__).parent

def get_respath(*parts: Union[str, Path]) -> str:
    """Get the absolute path to a resource (POSIX format).

    Args:
        *parts: Path components relative to the package root.

    Returns:
        str: The absolute POSIX path to the resource.
    """
    return (ROOT_PATH / Path(*parts)).as_posix()

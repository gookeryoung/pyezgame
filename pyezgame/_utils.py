from pathlib import Path

ROOT_PATH = Path(__file__).parent

def get_respath(resource: str) -> Path:
    """Get the absolute path to a resource.

    Args:
        resource (str): The name of the resource.

    Returns:
        Path: The absolute path to the resource.
    """
    resource_path = ROOT_PATH / resource
    if resource_path.exists():
        return resource_path.as_posix()
    return resource_path.as_posix()

# App Imports
from pathlib import Path

def get_project_root() -> Path:
    """
    Get the root directory of the project.

    Returns:
        Path: The absolute path to the project's root directory,
              assumed to be the parent of the parent of this file.

    Example:
        >>> root = get_project_root()
        >>> print(root)
        /path/to/project
    """
    # Current file's path
    current_file = Path(__file__)
    
    # Return the grandparent directory as the project root
    return current_file.parent.parent

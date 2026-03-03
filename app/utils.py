# App Imports
from pathlib import Path


def get_project_root() -> Path:
    current_file = Path(__file__)
    return current_file.parent.parent

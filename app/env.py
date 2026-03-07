# Python Modules
import os
from decimal import Decimal


def env_bool(name: str, default: bool) -> bool:
    """
    Read a boolean value from an environment variable.

    If the variable is not set, the provided default value is returned.

    Accepted truthy values (case-insensitive):
    - "true"
    - "1"
    - "yes"

    Any other value is treated as False.

    Parameters
    ----------
    name : str
        Name of the environment variable.
    default : bool
        Default value returned if the variable is not defined.

    Returns
    -------
    bool
        Parsed boolean value from the environment.
    """
    value = os.getenv(name)

    # If the environment variable does not exist, use the default
    if value is None:
        return default

    # Normalize the string and check for truthy values
    return value.lower() in {"true", "1", "yes"}


def env_int(name: str, default: int) -> int:
    """
    Read an integer value from an environment variable.

    If the variable is not defined, the provided default value is used.

    Parameters
    ----------
    name : str
        Name of the environment variable.
    default : int
        Default integer value if the variable is not set.

    Returns
    -------
    int
        Parsed integer value.
    """
    return int(os.getenv(name, default))


def env_decimal(name: str, default: str) -> Decimal:
    """
    Read a Decimal value from an environment variable.

    This is useful for numeric configuration values that require
    high precision (e.g., financial or scientific calculations).

    Parameters
    ----------
    name : str
        Name of the environment variable.
    default : str
        Default value used if the variable is not set. It must be a
        valid string representation of a decimal number.

    Returns
    -------
    Decimal
        Parsed Decimal value.
    """
    return Decimal(os.getenv(name, default))


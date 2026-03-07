# Python Modules
import pytest
from colorama import Fore

# App Imports
from app.console import Console, SingletonMeta
from app.exceptions import ConfigurationError


def reset_console():
    """Reset singleton instance so tests start clean."""
    SingletonMeta._instances = {}


def test_console_already_configured():
    """
    When console is configured, setup should raise ConfigurationError.
    """
    reset_console()
    console = Console()
    console.setup(enable_color=False)
    with pytest.raises(ConfigurationError):
        console.setup()


def test_console_not_configured(capsys):
    """
    When console is not configured, cprint should raise ConfigurationError.
    """
    reset_console()
    console = Console()
    with pytest.raises(ConfigurationError):
        console.cprint("message")


def test_cprint_with_color_branch(capsys):
    """
    When color is enabled, message should print with color codes.
    """
    reset_console()
    console = Console()
    console.setup(enable_color=True)

    console.cprint("plain message", Fore.RED)

    captured = capsys.readouterr()
    assert captured.out.strip() == "plain message"


def test_cprint_without_color_branch(capsys):
    """
    When color is disabled, message should print without color codes.
    """
    reset_console()
    console = Console()
    console.setup(enable_color=False)

    console.cprint("plain message")

    captured = capsys.readouterr()
    assert captured.out.strip() == "plain message"


def test_warning_method(capsys):
    """
    warning() should call cprint with yellow.
    """
    reset_console()
    console = Console()
    console.setup(enable_color=False)

    console.warning("warning message")

    captured = capsys.readouterr()
    assert "warning message" in captured.out


def test_info_method(capsys):
    """
    info() should call cprint with cyan.
    """
    reset_console()
    console = Console()
    console.setup(enable_color=False)

    console.info("info message")

    captured = capsys.readouterr()
    assert "info message" in captured.out

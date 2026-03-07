# Python Modules
import colorama
from colorama import Fore, Style

# Datatypes
from typing import Optional

# App Imports
from app.exceptions import ConfigurationError


class SingletonMeta(type):
    """
    Metaclass implementing the Singleton pattern.

    Any class using this metaclass will only have a single instance
    throughout the application's lifetime. Subsequent instantiations
    return the same existing object.

    This is used to ensure that global services such as the console
    output manager are shared consistently across the application.
    """

    # Stores created singleton instances per class
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Control instance creation.

        If an instance of the class already exists, return it.
        Otherwise create a new one and store it.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Console(metaclass=SingletonMeta):
    """
    Console utility for formatted terminal output.

    This class provides a centralized way to print colored messages
    using the `colorama` library. It also ensures a single shared
    instance across the application using the Singleton pattern.

    The console must be initialized using `setup()` before use.
    """
    def __init__(self):
        super().__init__()
        self.initiated: bool = False

    
    def setup(self, enable_color: bool = True) -> None:
        """
        Initialize the console output system.

        This sets up colorama and determines whether colored
        output should be enabled.

        Parameters
        ----------
        enable_color : bool
            Whether colored text output should be enabled.

        Raises
        ----------
        ConfigurationError
            If setup was done before.
        """
        if self.initiated:
            raise ConfigurationError("Console already configured.")
        
        colorama.init(autoreset=True)
        self.enable_color = enable_color
        self.initiated = True


    def cprint(self, message: str, color: Optional[str] = None) -> None:
        """
        Print a message to the terminal with optional color.

        Parameters
        ----------
        message : str
            Text message to display.
        color : Optional[str]
            Color from `colorama.Fore` to apply to the message.

        Raises
        ----------
        ConfigurationError
            If setup wasn't called before calling the method.
        """
        if not self.initiated:
            raise ConfigurationError("Call setup before printing.")
        
        # Apply color formatting only if enabled
        if self.enable_color and color:
            print(f"{color}{message}{Style.RESET_ALL}")
        else:
            print(message)

    def success(self, msg: str) -> None:
        """
        Print a success message in green.
        """
        self.cprint(msg, Fore.GREEN)

    def error(self, msg: str) -> None:
        """
        Print an error message in red.
        """
        self.cprint(msg, Fore.RED)

    def warning(self, msg: str) -> None:
        """
        Print a warning message in yellow.
        """
        self.cprint(msg, Fore.YELLOW)

    def info(self, msg: str) -> None:
        """
        Print an informational message in cyan.
        """
        self.cprint(msg, Fore.CYAN)

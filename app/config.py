# Python Modules
import os
from pathlib import Path
from dotenv import load_dotenv
from abc import ABC, abstractmethod

# Datatypes
from typing import Optional
from numbers import Number

# App imports
from app.utils import get_project_root
from app.exceptions import ConfigurationError
from app.env import env_bool, env_int, env_decimal


# Load environment variables from .env file
load_dotenv()


class Config(ABC):
    """
    Base configuration interface.

    All configuration classes must implement a validation step
    to ensure that loaded values are valid before the application
    begins execution.
    """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate configuration values.

        Implementations should raise an exception if any value
        is invalid.
        """
        pass  # pragma: no cover


class CalculatorConfig(Config):
    """
    Configuration for the Calculator application.

    Configuration values are resolved in the following priority order:

    1. Explicit parameters passed to the constructor
    2. Environment variables
    3. Default values

    The class also exposes commonly used filesystem paths such as
    log and history storage locations.
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None,
    ):
        """
        Initialize calculator configuration.

        Parameters
        ----------
        base_dir : Optional[Path]
            Base directory used for storing logs and history files.
        max_history_size : Optional[int]
            Maximum number of history records retained.
        auto_save : Optional[bool]
            Whether calculation history should automatically persist.
        precision : Optional[int]
            Decimal precision used for calculations.
        max_input_value : Optional[Number]
            Maximum allowed numeric input value.
        default_encoding : Optional[str]
            Encoding used when reading and writing files.
        """

        project_root = get_project_root()

        # Base directory used for application data
        self.base_dir = base_dir or Path(
            os.getenv("CALCULATE_BASE_DIR", str(project_root))
        )

        # Maximum number of stored history records
        self.max_history_size = max_history_size or env_int(
            "CALCULATOR_MAX_HISTORY_SIZE", "1000"
        )

        # Whether history is automatically saved
        self.auto_save = auto_save or env_bool(
            "CALCULATOR_AUTO_SAVE", "true"
        )

        # Decimal precision used during calculations
        self.precision = precision or env_int(
            "CALCULATOR_PRECISION", "10"
        )

        # Maximum permitted numeric input
        self.max_input_value = max_input_value or env_decimal(
            "CALCULATOR_MAX_INPUT_VALUE", "1e999"
        )

        # Default file encoding
        self.default_encoding = default_encoding or os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

    @property
    def log_dir(self) -> Path:
        """
        Directory where application log files are stored.
        """
        return Path(
            os.getenv(
                "CALCULATOR_LOG_DIR",
                str(self.base_dir / "logs"),
            )
        ).resolve()

    @property
    def log_file(self) -> Path:
        """
        Full path to the calculator log file.
        """
        return Path(
            os.getenv(
                "CALCULATOR_LOG_FILE",
                str(self.log_dir / "calculator.log"),
            )
        ).resolve()

    @property
    def history_dir(self) -> Path:
        """
        Directory where calculation history files are stored.
        """
        return Path(
            os.getenv(
                "CALCULATOR_HISTORY_DIR",
                str(self.base_dir / "history"),
            )
        ).resolve()

    @property
    def history_file(self) -> Path:
        """
        Full path to the calculation history CSV file.
        """
        return Path(
            os.getenv(
                "CALCULATOR_HISTORY_FILE",
                str(self.history_dir / "calculator_history.csv"),
            )
        ).resolve()

    def validate(self) -> None:
        """
        Validate configuration values.

        Raises
        ------
        ConfigurationError
            If any configuration value is invalid.
        """

        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")

        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")

        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")


class ReplConfig(Config):
    """
    Configuration for the REPL interface.
    """

    def __init__(self, color_text: Optional[bool] = None):
        """
        Initialize REPL configuration.

        Parameters
        ----------
        color_text : Optional[bool]
            Whether terminal output should use colored text.
        """

        self.color_text = color_text or env_bool(
            "REPL_COLOR_TEXT", "true"
        )

    def validate(self) -> None:
        """
        Validate REPL configuration.

        Currently no validation rules are required.
        """
        return

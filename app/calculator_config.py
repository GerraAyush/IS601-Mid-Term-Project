# Python Modules
import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# Datatypes
from typing import Optional
from decimal import Decimal
from numbers import Number

# App imports
from app.exceptions import ConfigurationError
from app.utils import get_project_root

# Load environment variables from .env file
load_dotenv()

@dataclass
class CalculatorConfig:
    """
    Configuration class for the Calculator application.

    This class loads configuration values either from:
    1. Explicit parameters passed during initialization, or
    2. Environment variables, or
    3. Default values if neither is provided.

    It also provides convenient properties for commonly used paths
    such as log files and history storage.
    """

    def __init__(
            self, 
            base_dir: Optional[Path] = None, 
            max_history_size: Optional[int] = None, 
            auto_save: Optional[bool] = None,
            precision: Optional[int] = None, 
            max_input_value: Optional[Number] = None, 
            default_encoding: Optional[str] = None
        ):
        """
        Initialize calculator configuration.

        Parameters
        ----------
        base_dir : Optional[Path]
            Base directory for application files.
        max_history_size : Optional[int]
            Maximum number of history records to store.
        auto_save : Optional[bool]
            Whether command history should automatically save.
        precision : Optional[int]
            Decimal precision used in calculations.
        max_input_value : Optional[Number]
            Maximum allowed numeric input value.
        default_encoding : Optional[str]
            Default encoding used for reading/writing files.
        """

        # Determine project root directory
        project_root = get_project_root()

        # Base directory where logs/history files are stored
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATE_BASE_DIR', str(project_root))
        )

        # Maximum number of stored calculation history records
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )

        # Determine whether auto-save is enabled
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        # Decimal precision used for calculations
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        # Maximum allowed input value for calculations
        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        # Default encoding used for files
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        """
        Directory where application logs are stored.
        """
        return Path(
            os.getenv(
                'CALCULATOR_LOG_DIR',
                str(self.base_dir / "logs")
            )
        ).resolve()
    
    @property
    def log_file(self) -> Path:
        """
        Full path to the calculator log file.
        """
        return Path(
            os.getenv(
                'CALCULATOR_LOG_FILE',
                str(self.log_dir / "calculator.log")
            )
        ).resolve()
    
    @property
    def history_dir(self) -> Path:
        """
        Directory where calculation history files are stored.
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        """
        Full path to the calculation history CSV file.
        """
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()
    
    def validate(self) -> None:
        """
        Validate configuration values.

        Raises
        ------
        ConfigurationError
            If any configuration value is invalid.
        """

        # Ensure history size is positive
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        
        # Ensure precision is positive
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")

        # Ensure maximum input value is positive
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")
        
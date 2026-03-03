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

load_dotenv()

@dataclass
class CalculatorConfig:
    def __init__(
            self, 
            base_dir: Optional[Path] = None, 
            max_history_size: Optional[int] = None, 
            auto_save: Optional[bool] = None,
            precision: Optional[int] = None, 
            max_input_value: Optional[Number] = None, 
            default_encoding: Optional[str] = None
        ):

        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATE_BASE_DIR', str(project_root))
        )

        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )

        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )

    @property
    def log_dir(self) -> Path:
        return Path(
            os.getenv(
                'CALCULATOR_LOG_DIR',
                str(self.base_dir / "logs")
            )
        ).resolve()
    
    @property
    def log_file(self) -> Path:
        return Path(
            os.getenv(
                'CALCULATOR_LOG_FILE',
                str(self.log_dir / "calculator.log")
            )
        ).resolve()
    
    @property
    def history_dir(self) -> Path:
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()

    @property
    def history_file(self) -> Path:
        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()
    
    def validate(self) -> None:
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")        
    
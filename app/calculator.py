# Datatypes
import os
import logging
import pandas as pd
from typing import List, Any, Optional

# App Imports
from app.datatypes import Number
from app.operation import Operation
from app.utils import get_project_root
from app.history import HistoryObserver
from app.calculation import Calculation
from app.validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import ValidationError, OperationError, ConfigurationError


class Calculator:
    def __init__(self, config: Optional[CalculatorConfig] = None):
        if config is None:
            project_root = get_project_root()
            config = CalculatorConfig(base_dir=project_root)

        self.config = config
        self.config.validate()

        self._setup_directories()

        self.operation_strategy: Optional[Operation] = None
        self.history: List[Calculation] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self._observers: List[HistoryObserver] = []

        self._setup_logging()

        logging.info("Calculator initialized with configuration")

    def _setup_logging(self):
        try:
            log_file = self.config.log_file.resolve()

            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True
            )
            logging.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            raise ConfigurationError(f"Configuration failed with error: {e}")
        
    def _setup_directories(self):
        os.makedirs(self.config.history_dir, exist_ok=True)
        os.makedirs(self.config.log_dir, exist_ok=True)

    def set_operation(self, operation_strategy: Operation):
        self.operation_strategy = operation_strategy
        logging.info(f"Set operation: {operation_strategy}")

    def show_history(self):
        if len(self.history) > 0:
            print("Following operations have been performed: ")
            for idx, calc in enumerate(self.history):
                print(f"{idx + 1}. {calc}")
        else:
            print("No operations in history.")

    def clear_history(self):
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def undo(self) -> bool:
        if len(self.undo_stack) == 0:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(history=self.history.copy()))
        self.history = memento.history.copy()
        return True
    
    def redo(self) -> bool:
        if len(self.redo_stack) == 0:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(history=self.history.copy()))
        self.history = memento.history.copy()
        return True

    def perform_operation(self, a: Any, b: Any) -> Number:
        if not self.operation_strategy:
            raise OperationError("No operation set")
        
        try:
            validated_a = InputValidator.validate_number(a)
            validated_b = InputValidator.validate_number(b)
            result = self.operation_strategy.execute(validated_a, validated_b)

            calculation = Calculation(
                _operation_name=self.operation_strategy.cmd,
                _operand1=validated_a,
                _operand2=validated_b,
            )
            self.undo_stack.append(CalculatorMemento(history=self.history.copy()))
            self.redo_stack.clear()
            
            self.history.append(calculation)

            self.notify_observers(calculation)

            return result
        
        except ValidationError as e:
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
    
    def add_observer(self, observer: HistoryObserver) -> None:
        self._observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: HistoryObserver) -> None:
        self._observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        [
            observer.update(calculation) for observer 
            in self._observers
        ]

    def save_history(self):
        try:
            history_data = [calculation.to_dict() for calculation in self.history]

            if history_data:
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
            else:
                pd.DataFrame(
                    columns=[
                        'operation_name', 
                        'operand1', 
                        'operand2', 
                        'operation_class',
                        'result', 
                        'timestamp'
                    ]
                ).to_csv(self.config.history_file, index=False)
                logging.info("Empty history saved")

        except Exception as e:
            logging.error(f"Failed to save history: {e}")
            raise OperationError(f"Failed to save history: {e}")
        
    def load_history(self):
        try:
            if self.config.history_file.exists():
                df = pd.read_csv(self.config.history_file)
                if not df.empty:
                    self.history = [
                        Calculation.from_dict(row.to_dict())
                        for _, row in df.iterrows()
                    ]
                    logging.info(f"Loaded {len(self.history)} calculations from history")
                else:
                    logging.info("Loaded empty history file")
            else:
                logging.info("No history file found - starting with empty history")
        except Exception as e:
            logging.error(f"Failed to load history: {e}")
            raise OperationError(f"Failed to load history: {e}")
        
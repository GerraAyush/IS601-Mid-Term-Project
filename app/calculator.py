# Python Modules
import os
import logging
import pandas as pd

# Datatypes
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
    """
    Core calculator class that manages operations, history, undo/redo stacks,
    observers, and persistence of calculation history.

    Features:
    - Set and perform operations
    - Track calculation history
    - Undo/redo functionality using memento pattern
    - Observer pattern support (history observers)
    - Save/load history to CSV
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize the calculator with optional configuration.

        Parameters
        ----------
        config : Optional[CalculatorConfig]
            Calculator configuration object. If None, a default configuration
            is created using the project root.

        Raises
        ------
        ConfigurationError
            If configuration or logging setup fails.
        """
        if config is None:
            project_root = get_project_root()
            config = CalculatorConfig(base_dir=project_root)

        self.config = config
        self.config.validate()
        
        # Ensure log and history directories exist
        self._setup_directories()

        # Current operation strategy (e.g., Addition, Subtraction)
        self.operation_strategy: Optional[Operation] = None

        # Full history of calculations
        self.history: List[Calculation] = []

        # Stacks for undo and redo operations (memento pattern)
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        # Observers to notify on new calculations
        self._observers: List[HistoryObserver] = []

        # Setup logging to file
        self._setup_logging()

        logging.info("Calculator initialized with configuration")

    def _setup_logging(self):
        """Setup logging to file as defined in the configuration."""
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
        """Ensure directories for logs and history exist."""
        os.makedirs(self.config.history_dir, exist_ok=True)
        os.makedirs(self.config.log_dir, exist_ok=True)

    def set_operation(self, operation_strategy: Operation):
        """
        Set the current operation strategy for the calculator.

        Parameters
        ----------
        operation_strategy : Operation
            An instance of an operation to perform on operands.
        """
        self.operation_strategy = operation_strategy
        logging.info(f"Set operation: {operation_strategy}")

    def show_history(self):
        """
        Display all calculations performed so far.
        If history is empty, notifies the user.
        """
        if len(self.history) > 0:
            print("Following operations have been performed: ")
            for idx, calc in enumerate(self.history):
                print(f"{idx + 1}. {calc}")
        else:
            print("No operations in history.")

    def clear_history(self):
        """
        Clear calculation history and reset undo/redo stacks.
        """
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        logging.info("History cleared")

    def undo(self) -> bool:
        """
        Undo the last operation by restoring from undo stack.

        Returns
        -------
        bool
            True if undo was successful, False if undo stack is empty.
        """
        if len(self.undo_stack) == 0:
            return False
        memento = self.undo_stack.pop()
        self.redo_stack.append(CalculatorMemento(history=self.history.copy()))
        self.history = memento.history.copy()
        return True
    
    def redo(self) -> bool:
        """
        Redo the last undone operation by restoring from redo stack.

        Returns
        -------
        bool
            True if redo was successful, False if redo stack is empty.
        """
        if len(self.redo_stack) == 0:
            return False
        memento = self.redo_stack.pop()
        self.undo_stack.append(CalculatorMemento(history=self.history.copy()))
        self.history = memento.history.copy()
        return True

    def perform_operation(self, a: Any, b: Any) -> Number:
        """
        Execute the current operation on given operands.

        Parameters
        ----------
        a : Any
            First operand
        b : Any
            Second operand

        Returns
        -------
        Number
            Result of the operation

        Raises
        ------
        OperationError
            If no operation is set or if operation execution fails.
        ValidationError
            If the input operands are invalid.
        """
        if not self.operation_strategy:
            raise OperationError("No operation set")
        
        try:
            # Validate operands
            validated_a = InputValidator.validate_number(a)
            validated_b = InputValidator.validate_number(b)

            # Execute operation
            result = self.operation_strategy.execute(validated_a, validated_b)

            # Record calculation in history
            calculation = Calculation(
                _operation_name=self.operation_strategy.cmd,
                _operand1=validated_a,
                _operand2=validated_b,
            )

            # Save current state to undo stack and clear redo stack
            self.undo_stack.append(CalculatorMemento(history=self.history.copy()))
            self.redo_stack.clear()
            
            self.history.append(calculation)

            # Notify observers of new calculation
            self.notify_observers(calculation)

            return result
        
        except ValidationError as e:
            logging.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Operation failed: {str(e)}")
            raise OperationError(f"Operation failed: {str(e)}")
    
    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Add an observer to be notified when a new calculation occurs.

        Parameters
        ----------
        observer : HistoryObserver
        """
        self._observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")
    
    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Remove an observer from the notification list.

        Parameters
        ----------
        observer : HistoryObserver
        """
        self._observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        Notify all observers about a new calculation.

        Parameters
        ----------
        calculation : Calculation
        """
        [
            observer.update(calculation) for observer 
            in self._observers
        ]

    def save_history(self):
        """
        Persist calculation history to CSV.

        Saves all calculations to the configured history file. 
        If history is empty, an empty CSV is created.
        Raises OperationError on failure.
        """
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
        """
        Load calculation history from CSV.

        If the history file does not exist, starts with empty history.
        Raises OperationError if loading fails.
        """
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
        
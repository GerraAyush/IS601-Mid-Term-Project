# Python Modules
import logging

# Datatypes
from abc import ABC, abstractmethod

# App imports
from app.calculation import Calculation


class HistoryObserver(ABC):
    """
    Abstract base class for observers that want to receive notifications
    when a new calculation is performed in the Calculator.
    """

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """
        Called when a new calculation is performed.

        Args:
            calculation (Calculation): The calculation that was just performed.
        """
        pass  # pragma: no cover


class LoggingObserver(HistoryObserver):
    """
    Observer that logs every calculation performed to the configured logger.
    """

    def update(self, calculation: Calculation) -> None:
        """
        Log the performed calculation.

        Args:
            calculation (Calculation): The calculation that was just performed.

        Raises:
            AttributeError: If the calculation is None.
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        logging.info(f"Calculation performed: {str(calculation)}")


class AutoSaveObserver(HistoryObserver):
    """
    Observer that automatically saves calculator history whenever
    a new calculation is performed, if auto_save is enabled.
    """

    def __init__(self, calculator: "Calculator") -> None:
        """
        Initialize the AutoSaveObserver.

        Args:
            calculator (Calculator): The calculator instance to observe.

        Raises:
            TypeError: If calculator is None.
        """
        if calculator is None:
            raise TypeError("Calculator cannot be None")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """
        Save calculator history automatically if auto_save is enabled.

        Args:
            calculation (Calculation): The calculation that was just performed.

        Raises:
            AttributeError: If the calculation is None.
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")

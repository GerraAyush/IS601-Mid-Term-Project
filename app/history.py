# Python Modules
import logging

# Datatypes
from abc import ABC, abstractmethod

# App imports
from app.calculation import Calculation


class HistoryObserver(ABC):

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        pass  # pragma: no cover

class LoggingObserver(HistoryObserver):

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        logging.info(f"Calculation performed: {str(calculation)}")

class AutoSaveObserver(HistoryObserver):

    def __init__(self, calculator: "Calculator") -> None:
        if calculator is None:
            raise TypeError("Calculator cannot be None")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")

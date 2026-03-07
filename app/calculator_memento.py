# Python Modules
import datetime

# Datatypes
from typing import List
from dataclasses import dataclass, field

# App imports
from app.calculation import Calculation


@dataclass
class CalculatorMemento:
    """
    Stores a snapshot of the calculator's state.

    This class implements the Memento design pattern, which allows the
    application to save and restore the calculator's history at a
    particular point in time without exposing its internal structure.

    Attributes
    ----------
    history : List[Calculation]
        A list of Calculation objects representing the calculator's history.
    timestamp : datetime.datetime
        The time when the snapshot was created.
    """

    # List of calculations representing the saved state of the calculator
    history: List[Calculation]

    # Timestamp automatically generated when the memento is created
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

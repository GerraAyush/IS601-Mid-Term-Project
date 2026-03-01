# Python Modules
import datetime

# Datatypes
from typing import List
from dataclasses import dataclass, field

# App imports
from app.calculation import Calculation


@dataclass
class CalculatorMemento:

    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

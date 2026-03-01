# Datatypes
from typing import List, Any

# App Imports
from app.datatypes import Number
from app.operation import Operation
from app.validators import InputValidator
from app.calculation import Calculation

class Calculator:
    def __init__(self):
        self.operation_strategy = None
        self.history: List[Calculation] = []

    def set_operation(self, operation_strategy: Operation):
        self.operation_strategy = operation_strategy

    def show_history(self):
        if len(self.history) > 0:
            print("Following operations have been performed: ")
            for idx, calc in enumerate(self.history):
                print(f"{idx + 1}. {calc}")
        else:
            print("No operations performed.")

    def clear_history(self):
        self.history.clear()

    def perform_operation(self, a: Any, b: Any) -> Number:
        validated_a = InputValidator.validate_number(a)
        validated_b = InputValidator.validate_number(b)
        result = self.operation_strategy.execute(validated_a, validated_b)

        calculation = Calculation(
            _operation_name=self.operation_strategy.cmd,
            _operand1=validated_a,
            _operand2=validated_b,
        )
        self.history.append(calculation)

        return result
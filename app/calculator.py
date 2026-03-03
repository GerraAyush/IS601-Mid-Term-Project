# Datatypes
import os
import pandas as pd
from typing import List, Any

# App Imports
from app.datatypes import Number
from app.operation import Operation
from app.validators import InputValidator
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import ValidationError, OperationError

class Calculator:
    def __init__(self, history_dir, history_file):
        self.operation_strategy = None
        self.history: List[Calculation] = []

        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        self.history_file = history_file
        self.history_dir = history_dir

    def set_operation(self, operation_strategy: Operation):
        self.operation_strategy = operation_strategy

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

            return result
        
        except ValidationError:
            raise
        except Exception as e:
            raise OperationError(f"Operation failed: {str(e)}")
        
    def save_history(self):
        try:
            os.makedirs(self.history_dir, exist_ok=True)

            history_data = [calculation.to_dict() for calculation in self.history]

            if history_data:
                df = pd.DataFrame(history_data)
                df.to_csv(self.history_file, index=False)
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
                ).to_csv(self.history_file, index=False)

        except Exception as e:
            raise OperationError(f"Failed to save history: {e}")
        
    def load_history(self):
        try:
            if self.history_file.exists():
                df = pd.read_csv(self.history_file)
                if not df.empty:
                    self.history = [
                        Calculation.from_dict({
                            'operation_name': row['operation_name'],
                            'operand1': row['operand1'],
                            'operand2': row['operand2'],
                            'operation_class': row['operation_class'],
                            'result': row['result'],
                            'timestamp': row['timestamp']
                        })
                        for _, row in df.iterrows()
                    ]
        except Exception as e:
            raise OperationError(f"Failed to load history: {e}")
        
# Datatypes
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

# App Imports
from app.datatypes import Number
from app.operation import OperationFactory
from app.exceptions import OperationError

@dataclass(frozen=True)
class Calculation:
    _operation_name: str
    _operand1: Number
    _operand2: Number

    _operation_class: str = field(init=False)
    _result: Number = field(init=False)
    _timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        operation = OperationFactory.create_operation(self._operation_name)

        object.__setattr__(
            self, 
            '_operation_class', 
            str(operation)
        )
        object.__setattr__(
            self, 
            '_result', 
            operation.execute(self._operand1, self._operand2)
        )

    def __str__(self) -> str:
        return f"{self._operation_class}({self._operand1}, {self._operand2}) = {self._result}"

    def __repr__(self) -> str:
        return (
            f"Calculation(operation_name='{self._operation_name}', "
            f"operand1={self._operand1}, "
            f"operand2={self._operand2}, "
            f"operation_class='{self._operation_class}', "
            f"result={self._result}, "
            f"timestamp='{self._timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self._operation_name == other._operation_name and
            self._operand1 == other._operand1 and
            self._operand2 == other._operand2 and
            self._result == other._result
        )

    def to_dict(self) -> Dict:
        return {
            'operation_name': self._operation_name,
            'operand1': self._operand1,
            'operand2': self._operand2,
            'operation_class': self._operation_class,
            'result': self._result,
            'timestamp': self._timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(calculation_dict: Dict[str, Any]) -> 'Calculation':
        try:
            return Calculation(
                _operation_name=calculation_dict['operation_name'],
                _operand1=calculation_dict['operand1'],
                _operand2=calculation_dict['operand2'],
                _timestamp=calculation_dict['timestamp']
            )
        except Exception as e:
            print(e)
            raise OperationError(f"Operation failed: {str(e)}")

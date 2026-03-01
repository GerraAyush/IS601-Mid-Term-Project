# Datatypes
from datetime import datetime
from dataclasses import dataclass, field

# App Imports
from app.datatypes import Number
from app.operation import OperationFactory

@dataclass(frozen=True)
class Calculation:
    _operation_name: str
    _operand1: Number
    _operand2: Number

    _operation_cls: str = field(init=False)
    _result: Number = field(init=False)
    _timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        operation = OperationFactory.create_operation(self._operation_name)

        object.__setattr__(
            self, 
            '_operation_cls', 
            str(operation)
        )
        object.__setattr__(
            self, 
            '_result', 
            operation.execute(self._operand1, self._operand2)
        )

    def __str__(self) -> str:
        return f"{self._operation_cls}({self._operand1}, {self._operand2}) = {self._result}"

    def __repr__(self) -> str:
        return (
            f"Calculation(operation='{self._operation_name}', "
            f"operand1={self._operand1}, "
            f"operand2={self._operand2}, "
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


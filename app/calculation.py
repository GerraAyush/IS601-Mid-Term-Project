# Datatypes
import logging
from typing import Dict, Any
from datetime import datetime
from dataclasses import dataclass, field

# App Imports
from app.datatypes import Number
from app.operation import OperationFactory
from app.exceptions import OperationError


@dataclass(frozen=True)
class Calculation:
    """
    Represents a single calculator operation and its result.

    This immutable data class stores:
    - The operation name (e.g., 'add', 'multiply')
    - The operands used for the calculation
    - The operation class name
    - The computed result
    - The timestamp when the calculation occurred

    The operation is executed automatically during object initialization
    using the OperationFactory.
    """

    # Input parameters required to perform the calculation
    _operation_name: str
    _operand1: Number
    _operand2: Number

    # Fields automatically computed after initialization
    _operation_class: str = field(init=False)
    _result: Number = field(init=False)

    # Timestamp of when the calculation was created
    _timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """
        Executes the operation after the dataclass has been initialized.

        Since the dataclass is frozen (immutable), object.__setattr__
        is used to set computed attributes.
        """

        # Create the operation instance using the factory
        operation = OperationFactory.create(self._operation_name)

        # Store the operation class name
        object.__setattr__(
            self, 
            '_operation_class', 
            str(operation)
        )

        # Execute the operation and store the result
        object.__setattr__(
            self, 
            '_result', 
            operation.execute(self._operand1, self._operand2)
        )

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the calculation.
        Example:
            Addition(2, 3) = 5
        """
        return f"{self._operation_class}({self._operand1}, {self._operand2}) = {self._result}"

    def __repr__(self) -> str:
        """
        Returns a detailed developer-friendly representation of the object.
        Useful for debugging and logging.
        """
        return (
            f"Calculation(operation_name='{self._operation_name}', "
            f"operand1={self._operand1}, "
            f"operand2={self._operand2}, "
            f"operation_class='{self._operation_class}', "
            f"result={self._result}, "
            f"timestamp='{self._timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Compares two Calculation objects for equality.

        Two calculations are considered equal if:
        - operation name matches
        - operands match
        - result matches
        Timestamp is intentionally ignored.
        """
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self._operation_name == other._operation_name and
            self._operand1 == other._operand1 and
            self._operand2 == other._operand2 and
            self._result == other._result
        )

    def to_dict(self) -> Dict:
        """
        Converts the calculation object into a dictionary.

        This is used for serialization (e.g., saving history to CSV).
        """
        return {
            'operation_name': self._operation_name,
            'operand1': self._operand1,
            'operand2': self._operand2,
            'operation_class': self._operation_class,
            'result': self._result,
            'timestamp': self._timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data_dict: Dict[str, Any]) -> 'Calculation':
        """
        Recreates a Calculation object from a dictionary.

        This method is primarily used when loading calculation history
        from persistent storage (e.g., CSV files).

        Parameters
        ----------
        data_dict : Dict[str, Any]
            Dictionary containing serialized calculation data.

        Returns
        -------
        Calculation
            Reconstructed Calculation instance.

        Raises
        ------
        OperationError
            If the calculation cannot be reconstructed.
        """
        try:
            calculation = Calculation(
                _operation_name=data_dict['operation_name'],
                _operand1=data_dict['operand1'],
                _operand2=data_dict['operand2'],
                _timestamp=datetime.fromisoformat(data_dict['timestamp'])
            )

            # Warn if stored result differs from recomputed result
            if calculation._result != data_dict["result"]:
                logging.warning(
                    f"Loaded calculation result {data_dict['result']} "
                    f"differs from computed result {calculation._result}"
                )
            return calculation

        except Exception as e:
            raise OperationError(f"Operation failed: {str(e)}")

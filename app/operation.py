# Datatypes
from typing import Any
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

# App imports
from app.datatypes import Number
from app.exceptions import ValidationError
from app.factory import FactoryBase


@dataclass(frozen=True)
class Operation(metaclass=ABCMeta):
    """
    Abstract base class for all calculator operations.

    Attributes:
        cmd (str): Command name to identify the operation.
    """
    cmd: str

    @abstractmethod
    def execute(self, a: Number, b: Number) -> Number:
        """
        Execute the operation on two operands.

        Args:
            a (Number): First operand.
            b (Number): Second operand.

        Returns:
            Number: Result of the operation.

        Raises:
            ValidationError: If operands are invalid (checked by `validate_operands`).
        """
        pass  # pragma: no cover

    def validate_operands(self, a: Number, b: Number) -> None:
        """
        Ensure that both operands are numbers.

        Args:
            a (Number): First operand.
            b (Number): Second operand.

        Raises:
            ValidationError: If either operand is not a number.
        """
        if not isinstance(a, Number) or not isinstance(b, Number):
            raise ValidationError("Operands must be numbers")
    
    def __str__(self) -> str:
        """Return the class name of the operation for readability."""
        return self.__class__.__name__


class Addition(Operation):
    """Performs a + b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a + b


class Subtraction(Operation):
    """Performs a - b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a - b


class Multiplication(Operation):
    """Performs a * b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a * b


class Division(Operation):
    """Performs a / b with division-by-zero validation."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a / b


class Power(Operation):
    """Performs a ** b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** b


class Root(Operation):
    """Performs the b-th root of a (a ** (1/b))."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Index cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** (1 / b)


class Modulus(Operation):
    """Performs a % b with zero-check for divisor."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a % b


class IntegerDivision(Operation):
    """Performs integer division a // b with zero-check."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a // b


class Percentage(Operation):
    """Calculates what percent a is of b."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Base cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculates the absolute difference |a - b|."""
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return abs(a - b)


class OperationFactory(FactoryBase):
    """
    Factory for creating operation instances from a command string.

    Example:
        op = OperationFactory.create('add', cmd='add')
        result = op.execute(2, 3)  # returns 5
    """

    # Map of command names to operation classes and descriptions
    _item_dict = {
        'add': {'_cls': Addition, 'desc': 'perform addition of two numbers'},
        'subtract': {'_cls': Subtraction, 'desc': 'perform subtraction of two numbers'},
        'multiply': {'_cls': Multiplication, 'desc': 'perform multiplication of two numbers'},
        'divide': {'_cls': Division, 'desc': 'perform division of a by b'},
        'power': {'_cls': Power, 'desc': 'perform a to the power of b'},
        'root': {'_cls': Root, 'desc': 'perform bth root of a'},
        'modulus': {'_cls': Modulus, 'desc': 'check divisibility of a wrt b'},
        'int_divide': {'_cls': IntegerDivision, 'desc': 'perform integer division of a by b'},
        'percent': {'_cls': Percentage, 'desc': 'check how much percent of b is a'},
        'abs_diff': {'_cls': AbsoluteDifference, 'desc': 'perform absolute difference of a and b'},
    }
    _base_class = Operation

    @classmethod
    def create(cls, name: str, **kwargs) -> Any:
        """
        Create an instance of the operation by name.

        Args:
            name (str): The name of the operation.
            **kwargs: Additional arguments for the operation constructor.

        Returns:
            Operation: An instance of the requested operation.

        Raises:
            ValueError: If the operation name is not registered.
        """
        info = cls._item_dict.get(name.lower())
        if not info:
            raise ValueError(f"Unregistered item: {name}")
        return info["_cls"](cmd=name, **kwargs)

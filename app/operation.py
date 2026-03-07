# Datatypes
from typing import Any
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

# App imports
from app.datatypes import Number
from app.exceptions import ValidationError
from app.factory import FactoryBase
from app.registry import operation


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


class OperationFactory(FactoryBase):
    """
    Factory for creating operation instances from a command string.

    Example:
        op = OperationFactory.create('add', cmd='add')
        result = op.execute(2, 3)  # returns 5
    """

    # Map of command names to operation classes and descriptions
    _item_dict = {}
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


@operation(name="add", description="perform addition of two numbers")
class Addition(Operation):
    """Performs a + b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a + b


@operation(name="subtract", description="perform subtraction of two numbers")
class Subtraction(Operation):
    """Performs a - b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a - b


@operation(name="multiply", description="perform multiplication of two numbers")
class Multiplication(Operation):
    """Performs a * b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a * b


@operation(name="divide", description="perform division of a by b")
class Division(Operation):
    """Performs a / b with division-by-zero validation."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a / b


@operation(name="power", description="perform a to the power of b")
class Power(Operation):
    """Performs a ** b."""
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** b


@operation(name="root", description="perform bth root of a")
class Root(Operation):
    """Performs the b-th root of a (a ** (1/b))."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Index cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** (1 / b)


@operation(name="modulus", description="check divisibility of a wrt b")
class Modulus(Operation):
    """Performs a % b with zero-check for divisor."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a % b


@operation(name="int_divide", description="perform integer division of a by b")
class IntegerDivision(Operation):
    """Performs integer division a // b with zero-check."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a // b


@operation(name="percent", description="check how much percent of b is a")
class Percentage(Operation):
    """Calculates what percent a is of b."""
    
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Base cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return (a / b) * 100


@operation(name="abs_diff", description="perform absolute difference of a and b")
class AbsoluteDifference(Operation):
    """Calculates the absolute difference |a - b|."""
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return abs(a - b)

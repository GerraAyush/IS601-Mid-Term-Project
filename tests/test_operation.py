# Python Modules
import pytest

# App Imports
from app.operation import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    Percentage,
    AbsoluteDifference,
    OperationFactory,
)
from app.exceptions import ValidationError


class CustomOp(Operation):
    """A custom operation for testing registration in the factory."""
    def execute(self, a, b):
        return a % b
    

@pytest.mark.parametrize(
    "op_cls,a,b,expected",
    [
        (Addition, 2, 3, 5),
        (Subtraction, 5, 3, 2),
        (Multiplication, 4, 3, 12),
        (Division, 10, 2, 5),
        (Power, 2, 3, 8),
        (Root, 9, 2, 3),
        (Modulus, 3, 4, 3),
        (IntegerDivision, 9, 2, 4),
        (Percentage, 2, 8, 25),
        (AbsoluteDifference, 4, 2, 2)
    ],
)
def test_operations_execute(op_cls, a, b, expected):
    """Verify that each operation returns the correct result."""
    op = op_cls(cmd="test")
    assert op.execute(a, b) == expected


def test_division_by_zero():
    """Division by zero should raise a ValidationError."""
    op = Division(cmd="divide")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(5, 0)


def test_root_index_zero():
    """Root index zero should raise a ValidationError."""
    op = Root(cmd="root")
    with pytest.raises(ValidationError, match="Index cannot be zero"):
        op.execute(9, 0)


def test_modulus_index_zero():
    """Modulus by zero should raise a ValidationError."""
    op = Modulus(cmd="modulus")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(9, 0)


def test_integer_division_index_zero():
    """Integer division by zero should raise a ValidationError."""
    op = IntegerDivision(cmd="int_divide")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(9, 0)


def test_percentage_index_zero():
    """Percentage with zero base should raise a ValidationError."""
    op = Percentage(cmd="percent")
    with pytest.raises(ValidationError, match="Base cannot be zero"):
        op.execute(9, 0)


def test_operation_str(addition_op):
    """Check that string representation returns operation name."""
    assert str(addition_op) == "Addition"


def test_is_registered_true():
    """Verify that known operations are registered (case-insensitive)."""
    assert OperationFactory.is_registered("add") is True
    assert OperationFactory.is_registered("ADD") is True


def test_is_registered_false():
    """Verify that unknown operations are not registered."""
    assert OperationFactory.is_registered("unknown") is False


def test_create_operation_success():
    """Creating a registered operation returns the correct instance."""
    op = OperationFactory.create("add")
    assert isinstance(op, Addition)
    assert op.cmd == "add"


def test_create_operation_unregistered():
    """Creating an unregistered operation should raise ValueError."""
    with pytest.raises(ValueError, match="Unregistered item"):
        OperationFactory.create("unknown_op")


def test_register_operation_success():
    """Registering a new operation dynamically works correctly."""
    OperationFactory.register(
        "mod",
        CustomOp,
        "modulo operation"
    )

    # Newly registered operation is recognized
    assert OperationFactory.is_registered("mod") is True
    op = OperationFactory.create("mod")
    assert isinstance(op, CustomOp)
    assert op.execute(5, 2) == 1


def test_register_operation_invalid_type():
    """Registering a class not inheriting from Operation should raise TypeError."""
    class NotOperation:
        pass

    with pytest.raises(TypeError, match="inherit from Operation"):
        OperationFactory.register(
            "bad",
            NotOperation,
            "bad operation"
        )


def test_list_operations_returns_string():
    """Listing operations returns a string description."""
    output = OperationFactory.list_items()
    assert isinstance(output, str)


def test_validate_operands_default_returns_none(addition_op):
    """Default validate_operands should return None without error."""
    assert addition_op.validate_operands(1, 2) is None

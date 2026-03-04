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
    op = op_cls(cmd="test")
    assert op.execute(a, b) == expected

def test_division_by_zero():
    op = Division(cmd="divide")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(5, 0)

def test_root_index_zero():
    op = Root(cmd="root")
    with pytest.raises(ValidationError, match="Index cannot be zero"):
        op.execute(9, 0)

def test_modulus_index_zero():
    op = Modulus(cmd="modulus")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(9, 0)

def test_integer_division_index_zero():
    op = IntegerDivision(cmd="int_divide")
    with pytest.raises(ValidationError, match="Divisor cannot be zero"):
        op.execute(9, 0)

def test_percentage_index_zero():
    op = Percentage(cmd="percent")
    with pytest.raises(ValidationError, match="Base cannot be zero"):
        op.execute(9, 0)

def test_operation_str():
    op = Addition(cmd="add")
    assert str(op) == "Addition"


def test_is_registered_true():
    assert OperationFactory.is_registered("add") is True
    assert OperationFactory.is_registered("ADD") is True  # case insensitive

def test_is_registered_false():
    assert OperationFactory.is_registered("unknown") is False

def test_create_operation_success():
    op = OperationFactory.create_operation("add")
    assert isinstance(op, Addition)
    assert op.cmd == "add"

def test_create_operation_unregistered():
    with pytest.raises(ValueError, match="Unregistered Operation"):
        OperationFactory.create_operation("unknown_op")

def test_register_operation_success():
    OperationFactory.register_operation(
        "mod",
        CustomOp,
        "modulo operation"
    )

    assert OperationFactory.is_registered("mod") is True
    op = OperationFactory.create_operation("mod")
    assert isinstance(op, CustomOp)
    assert op.execute(5, 2) == 1

def test_register_operation_invalid_type():
    class NotOperation:
        pass

    with pytest.raises(TypeError, match="inherit from Operation"):
        OperationFactory.register_operation(
            "bad",
            NotOperation,
            "bad operation"
        )

def test_list_operations_returns_string():
    output = OperationFactory.list_operations()
    assert isinstance(output, str)

def test_validate_operands_default_returns_none():
    op = Addition(cmd="add")
    assert op.validate_operands(1, 2) is None
    
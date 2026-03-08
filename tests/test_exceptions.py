# Python Modules
import pytest

# App Imports
from app.exceptions import CalculatorError, OperationError


def test_calculator_error_is_exception():
    """Ensure CalculatorError behaves like a standard Exception."""
    err = CalculatorError("base error")

    # Should inherit from Python's base Exception
    assert isinstance(err, Exception)
    assert str(err) == "base error"


def test_operation_error_inherits_calculator_error():
    """Ensure OperationError inherits from CalculatorError."""
    err = OperationError("operation failed")

    # Verify inheritance chain
    assert isinstance(err, OperationError)
    assert isinstance(err, CalculatorError)
    assert isinstance(err, Exception)
    assert str(err) == "operation failed"


def test_raise_calculator_error():
    """Ensure CalculatorError can be raised and caught."""
    with pytest.raises(CalculatorError, match="boom"):
        raise CalculatorError("boom")


def test_raise_operation_error_caught_as_base():
    """Ensure OperationError can be caught as its base class."""
    with pytest.raises(CalculatorError):
        raise OperationError("child error")


def test_raise_operation_error_specific():
    """Ensure OperationError can be caught specifically."""
    with pytest.raises(OperationError, match="specific"):
        raise OperationError("specific")

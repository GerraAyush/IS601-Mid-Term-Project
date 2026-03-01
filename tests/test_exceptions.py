# Python Modules
import pytest

# App Imports
from app.exceptions import CalculatorError, OperationError


def test_calculator_error_is_exception():
    err = CalculatorError("base error")
    assert isinstance(err, Exception)
    assert str(err) == "base error"

def test_operation_error_inherits_calculator_error():
    err = OperationError("operation failed")
    assert isinstance(err, OperationError)
    assert isinstance(err, CalculatorError)
    assert isinstance(err, Exception)
    assert str(err) == "operation failed"

def test_raise_calculator_error():
    with pytest.raises(CalculatorError, match="boom"):
        raise CalculatorError("boom")

def test_raise_operation_error_caught_as_base():
    with pytest.raises(CalculatorError):
        raise OperationError("child error")

def test_raise_operation_error_specific():
    with pytest.raises(OperationError, match="specific"):
        raise OperationError("specific")
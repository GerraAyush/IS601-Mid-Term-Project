# Python Modules
import pytest
from unittest.mock import patch

# App Imports
from app.calculator import Calculator
from app.operation import Addition
from app.calculation import Calculation
from app.exceptions import OperationError


@pytest.fixture
def calculator():
    return Calculator()

@pytest.fixture
def addition_op():
    return Addition(cmd="add")

def test_set_operation(calculator, addition_op):
    calculator.set_operation(addition_op)
    assert calculator.operation_strategy is addition_op

def test_perform_operation_success(calculator, addition_op):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]):
        result = calculator.perform_operation(2, 3)

    assert result == 5
    assert len(calculator.history) == 1

    calc = calculator.history[0]
    assert isinstance(calc, Calculation)
    assert calc._operand1 == 2
    assert calc._operand2 == 3
    assert calc._operation_name == "add"

def test_perform_operation_uses_validator(calculator, addition_op):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number") as mock_validator:
        mock_validator.side_effect = [10, 20]
        calculator.perform_operation("10", "20")

        assert mock_validator.call_count == 2
        mock_validator.assert_any_call("10")
        mock_validator.assert_any_call("20")

def test_history_appends_multiple(calculator, addition_op):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2, 3, 4]):
        calculator.perform_operation(1, 2)
        calculator.perform_operation(3, 4)

    assert len(calculator.history) == 2

def test_clear_history(calculator, addition_op):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]):
        calculator.perform_operation(2, 3)

    assert len(calculator.history) == 1

    calculator.clear_history()
    assert calculator.history == []

def test_show_history_empty(calculator, capsys):
    calculator.show_history()
    captured = capsys.readouterr()
    assert "No operations in history." in captured.out

def test_show_history_with_entries(calculator, addition_op, capsys):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number", side_effect=[5, 6]):
        calculator.perform_operation(5, 6)

    calculator.show_history()
    captured = capsys.readouterr()

    assert "Following operations have been performed:" in captured.out
    assert "1." in captured.out

def test_perform_operation_without_strategy(calculator):
    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2]):
        with pytest.raises(OperationError, match="No operation set"):
            calculator.perform_operation(1, 2)
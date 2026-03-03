# Python Modules
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch, PropertyMock
from tempfile import TemporaryDirectory

# App Imports
from app.operation import Addition
from app.calculator import Calculator
from app.calculation import Calculation
from app.exceptions import OperationError
from app.calculator_config import CalculatorConfig


@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            yield Calculator(config=config)

def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")

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

    calculation = calculator.history[0]
    assert isinstance(calculation, Calculation)
    assert calculation._operand1 == 2
    assert calculation._operand2 == 3
    assert calculation._operation_name == "add"
    assert calculation._operation_class == "Addition"
    assert calculation._result == 5
    
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

def test_save_history_empty(calculator):
    calculator.save_history()
    assert calculator.config.history_file.exists()

def test_save_history_with_data(calculator):
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]):
        calculator.perform_operation(2, 3)

    calculator.save_history()
    assert calculator.config.history_file.exists()

def test_save_history_exception(calculator):
    with patch("pandas.DataFrame.to_csv", side_effect=Exception("boom")):
        with pytest.raises(OperationError, match="Failed to save history"):
            calculator.save_history()

def test_load_history_file_not_exists(calculator):
    calculator.load_history()
    assert calculator.history == []

def test_load_history_with_data(calculator):
    df = pd.DataFrame([{
        "operation_name": "add",
        "operand1": 2,
        "operand2": 3,
        "operation_class": "Addition",
        "result": 5,
        "timestamp": "2024-01-01T00:00:00"
    }])

    with patch("app.calculator.pd.read_csv", return_value=df), \
         patch("pathlib.Path.exists", return_value=True), \
         patch("app.calculator.Calculation.from_dict") as mock_from_dict:

        mock_from_dict.return_value = "mocked_calc"

        calculator.load_history()

        assert calculator.history == ["mocked_calc"]

def test_load_history_exception(calculator):
    with patch("app.calculator.pd.read_csv", side_effect=Exception("boom")), \
         patch("pathlib.Path.exists", return_value=True):

        with pytest.raises(OperationError, match="Failed to load history"):
            calculator.load_history()

def test_perform_operation_wraps_exception(calculator):
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]), \
         patch("app.operation.Addition.execute", side_effect=Exception("boom")):

        with pytest.raises(OperationError, match="Operation failed: boom"):
            calculator.perform_operation(2, 3)

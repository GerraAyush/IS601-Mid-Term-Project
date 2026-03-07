# Python Modules
import pytest
import logging
import pandas as pd
from pathlib import Path
from unittest.mock import patch, PropertyMock, Mock

# App Imports
from app.operation import Addition
from app.calculator import Calculator
from app.calculation import Calculation
from app.exceptions import OperationError, ConfigurationError
from app.config import CalculatorConfig
from app.history import LoggingObserver


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

def test_show_history_empty(calculator):
    output = calculator.show_history()
    assert "No operations in history." in output

def test_show_history_with_entries(calculator, addition_op):
    calculator.set_operation(addition_op)

    with patch("app.calculator.InputValidator.validate_number", side_effect=[5, 6]):
        calculator.perform_operation(5, 6)

    output = calculator.show_history()

    assert "Following operations have been performed:" in output
    assert "1." in output

def test_perform_operation_without_strategy(calculator):
    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2]):
        with pytest.raises(OperationError, match="No operation set"):
            calculator.perform_operation(1, 2)


def test_save_history_empty(calculator):
    calculator.save_history()
    assert calculator.config.history_file.exists()

def test_save_history_with_data(addition_op, calculator):
    calculator.set_operation(addition_op)

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

def test_load_history_failure(calculator, monkeypatch):
    monkeypatch.setattr("pathlib.Path.exists", True)
    monkeypatch.setattr("pandas.read_csv", lambda *args, **kwargs: (_ for _ in ()).throw(Exception("CSV broke")))

    with pytest.raises(OperationError):
        calculator.load_history()

def test_load_history_logging(calculator, caplog):
    with caplog.at_level(logging.INFO):
        calculator.save_history()
        calculator.load_history()
        assert "Loaded empty history file" in caplog.text

def test_perform_operation_wraps_exception(calculator):
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]), \
         patch("app.operation.Addition.execute", side_effect=Exception("boom")):

        with pytest.raises(OperationError, match="Operation failed: boom"):
            calculator.perform_operation(2, 3)

def test_calculator_default_config(monkeypatch):
    monkeypatch.setattr("app.calculator.get_project_root", lambda: Path("."))
    calc = Calculator(config=None)
    assert calc is not None

def test_setup_logging_failure(monkeypatch):
    config = CalculatorConfig(base_dir=Path("."))

    def broken_logging(*args, **kwargs):
        raise Exception("Logging broke")

    monkeypatch.setattr("logging.basicConfig", broken_logging)

    with pytest.raises(ConfigurationError):
        Calculator(config)

def test_perform_operation_generic_failure(calculator):
    fake_operation = Mock()
    fake_operation.execute.side_effect = Exception("Boom")
    fake_operation.cmd = "add"

    calculator.set_operation(fake_operation)

    with pytest.raises(OperationError):
        calculator.perform_operation(5, 5)

def test_remove_observers(calculator, caplog):
    with caplog.at_level(logging.INFO):
        observer = LoggingObserver()
        calculator.add_observer(observer)
        calculator.remove_observer(observer)
        assert observer not in calculator._observers
        assert f"Removed observer: {observer.__class__.__name__}" in caplog.text

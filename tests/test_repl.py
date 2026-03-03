# Python Modules
import pytest
from pathlib import Path
from unittest.mock import patch, PropertyMock
from tempfile import TemporaryDirectory

# App Imports
from app.operation import Addition
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.calculator_repl import calculator_repl, print_operations


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

def test_print_operations(capsys):
    print_operations()
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out
    assert "add - perform addition of two numbers" in captured.out
    assert "subtract - perform subtraction of two numbers" in captured.out
    assert "multiply - perform multiplication of two numbers" in captured.out
    assert "divide - perform division of a by b" in captured.out
    assert "power - perform a to the power of b" in captured.out
    assert "root - perform bth root of a" in captured.out
    assert "modulus - check divisibility of a wrt b" in captured.out
    assert "idivide - perform integer division of a by b" in captured.out
    assert "percentage - check how much percent of b is a" in captured.out
    assert "abs-diff - perform absolute difference of a and b" in captured.out
    assert "exit - Exit the calculator" in captured.out

def test_repl_help_then_exit():
    inputs = iter(["help", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

def test_repl_history_then_exit():
    inputs = iter(["history", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

def test_repl_clear_then_exit(capsys):
    inputs = iter(["clear", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "Cleared history." in captured.out

def test_clear_history_clears_stacks(calculator, mocker):
    calculator.set_operation(Addition(cmd="add"))

    mocker.patch(
        "app.calculator.InputValidator.validate_number",
        side_effect=[2, 3]
    )

    calculator.perform_operation(2, 3)

    assert len(calculator.undo_stack) == 1

    calculator.clear_history()

    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []

def test_repl_invalid_operation(capsys):
    inputs = iter(["invalid_cmd", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "Unknown command: 'invalid_cmd'. Type 'help' for available commands." in captured.out

def test_repl_valid_operation_add(capsys):
    inputs = iter([
        "add",  # operation
        "2",    # operand1
        "3",    # operand2
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "Result: 5" in captured.out

def test_repl_undo_successful(capsys):
    inputs = iter([
        "add",
        "2",
        "3",
        "undo",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "Undo successful!" in captured.out

def test_repl_no_undo(capsys):
    inputs = iter([
        "undo",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "Nothing to undo" in captured.out

def test_repl_redo_successful(capsys):
    inputs = iter([
        "add",
        "2",
        "3",
        "undo",
        "redo",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "Redo successful!" in captured.out

def test_repl_no_redo(capsys):
    inputs = iter([
        "redo",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "Nothing to redo" in captured.out

def test_undo_empty_stack(calculator):
    assert calculator.undo() is False

def test_redo_empty_stack(calculator):
    assert calculator.redo() is False

def test_undo_modifies_history(calculator, mocker):
    calculator.set_operation(Addition(cmd="add"))

    mocker.patch(
        "app.calculator.InputValidator.validate_number",
        side_effect=[1, 2]
    )

    calculator.perform_operation(1, 2)

    assert len(calculator.history) == 1

    assert calculator.undo() is True
    assert calculator.history == []

def test_redo_restores_history(calculator, mocker):
    calculator.set_operation(Addition(cmd="add"))

    mocker.patch(
        "app.calculator.InputValidator.validate_number",
        side_effect=[1, 2]
    )

    calculator.perform_operation(1, 2)
    calculator.undo()

    assert calculator.history == []

    assert calculator.redo() is True
    assert len(calculator.history) == 1

def test_repl_exit(capsys):
    inputs = iter(["exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "GoodBye! Exiting" in captured.out

def test_repl_save_successful(capsys):
    inputs = iter([
        "add",
        "2",
        "3",
        "save",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "History saved successfully" in captured.out

def test_repl_load_successful(capsys):
    inputs = iter([
        "add",
        "2",
        "3",
        "save",
        "load",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()
    
    captured = capsys.readouterr()
    assert "History loaded successfully" in captured.out

def test_perform_operation_without_setting_operation(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(1, 2)

def test_perform_operation_validation_error_passthrough(calculator, mocker):
    calculator.set_operation(Addition(cmd="add"))

    mocker.patch(
        "app.calculator.InputValidator.validate_number",
        side_effect=ValidationError("Invalid input")
    )

    with pytest.raises(ValidationError):
        calculator.perform_operation("bad", 2)

def test_perform_operation_wraps_generic_exception(calculator, mocker):
    calculator.set_operation(Addition(cmd="add"))

    mocker.patch(
        "app.calculator.InputValidator.validate_number",
        side_effect=[1, 2]
    )

    mocker.patch.object(
        Addition,
        "execute",
        side_effect=Exception("boom")
    )

    with pytest.raises(OperationError, match="Operation failed: boom"):
        calculator.perform_operation(1, 2)

def test_save_history_exception(calculator, mocker):
    mocker.patch("pandas.DataFrame.to_csv", side_effect=Exception("fail"))

    with pytest.raises(OperationError):
        calculator.save_history()

def test_load_history_exception(calculator, mocker):
    calculator.save_history()
    
    mocker.patch("pandas.read_csv", side_effect=Exception("fail"))

    with pytest.raises(OperationError):
        calculator.load_history()

def test_exit_command(mocker):
    mocker.patch("builtins.input", side_effect=["exit"])
    mocker.patch("sys.exit", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        calculator_repl()

def test_keyboard_interrupt(mocker):
    mocker.patch(
        "builtins.input",
        side_effect=[KeyboardInterrupt, "exit"]
    )
    mocker.patch("sys.exit", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        calculator_repl()

def test_eof_error(mocker):
    mocker.patch("builtins.input", side_effect=EOFError)
    calculator_repl()

def test_invalid_operand(mocker):
    mocker.patch("builtins.input", side_effect=[
        "add",     # operation
        "abc",     # invalid operand
        "exit"     # exit after error
    ])
    mocker.patch("sys.exit", side_effect=SystemExit)

    with pytest.raises(SystemExit):
        calculator_repl()
        
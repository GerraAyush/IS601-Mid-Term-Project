# Python Modules
import pytest
from pathlib import Path
from unittest.mock import Mock
from tempfile import TemporaryDirectory
from unittest.mock import patch, PropertyMock

# App Imports
from app.command import (
    CalculationCommand,
    SaveCommand, 
    LoadCommand, 
    ExitCommand, 
    HelpCommand,
    ReplCommandFactory
)
from app.calculator import Calculator
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


def test_print_operations(capsys):
    HelpCommand().execute()
    captured = capsys.readouterr()
    commands = [
        "Available commands", "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide", "percent", "abs_diff",
        "help", "history", "clear", "undo", "redo", "save", "load", "exit",
    ]
    for command in commands:
        assert command in captured.out


def test_save_command_exception():
    calculator = Mock()
    calculator.save_history.side_effect = Exception("Save failed")

    cmd = SaveCommand(calculator)
    cmd.execute()  # should not raise

    calculator.save_history.assert_called_once()


def test_load_command_exception():
    calculator = Mock()
    calculator.load_history.side_effect = Exception("Load failed")

    cmd = LoadCommand(calculator)
    cmd.execute()

    calculator.load_history.assert_called_once()


def test_exit_command_with_on_exit(mocker):
    mock_exit = mocker.patch("sys.exit")

    help_cmd = HelpCommand()
    exit_cmd = ExitCommand()

    exit_cmd.execute(on_exit_command=help_cmd)
    mock_exit.assert_called_once()


def test_add_command_with_on_exit(calculator, mocker):
    mock_exit = mocker.patch("sys.exit")

    exit_cmd = ExitCommand()
    add_cmd = CalculationCommand(calculator, "add", 2, 3)

    exit_cmd.execute(on_exit_command=add_cmd)
    mock_exit.assert_called_once()


def test_exit_command_invalid_type():
    exit_cmd = ExitCommand()

    with pytest.raises(TypeError):
        exit_cmd.execute(on_exit_command="not_a_command")


def test_exit_command_cannot_accept_exit():
    exit_cmd = ExitCommand()

    with pytest.raises(TypeError):
        exit_cmd.execute(on_exit_command=ExitCommand())


def test_calculation_command():
    calculator = Mock()
    calculator.perform_operation.return_value = 10

    cmd = CalculationCommand(calculator, "add", 5, 5)
    result = cmd.execute()

    assert result == 10
    calculator.set_operation.assert_called_once()
    calculator.perform_operation.assert_called_once_with(5, 5)


def test_create_unregistered_item_raises(calculator):
    with pytest.raises(ValueError, match="Unregistered item: unknown"):
        ReplCommandFactory.create("unknown", calculator=calculator)

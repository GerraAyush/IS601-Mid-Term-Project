# Python Modules
import pytest
import logging
from unittest.mock import Mock, patch


# App Imports
from app.command import (
    CalculationCommand,
    SaveCommand, 
    LoadCommand, 
    ExitCommand, 
    HelpCommand,
    ReplCommandFactory
)

def test_print_operations():
    output = HelpCommand().execute()
    commands = [
        "Available commands", "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide", "percent", "abs_diff",
        "help", "history", "clear", "undo", "redo", "save", "load", "exit",
    ]
    for command in commands:
        assert command in output


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


def test_exception_save(calculator, caplog):
    with caplog.at_level(logging.INFO):
        with patch("app.calculator.Calculator.save_history", side_effect=Exception("Simulated Error")):
            with pytest.raises(Exception):
                SaveCommand(calculator).execute()
        
        assert "Error: " in caplog.text


def test_exception_load(calculator, caplog):
    with caplog.at_level(logging.INFO):
        with patch("app.calculator.Calculator.load_history", side_effect=Exception("Simulated Error")):
            with pytest.raises(Exception):
                LoadCommand(calculator).execute()
        
        assert "Error: " in caplog.text

# Python Modules
import pytest
import logging
from unittest.mock import Mock, patch


# App Imports
from app.command import (
    CalculationCommand,
    SaveCommand,
    LoadCommand,
    HelpCommand,
    ReplCommandFactory
)


def test_print_operations():
    """Ensure HelpCommand lists all available commands."""
    output = HelpCommand().execute()

    commands = [
        "Available commands", "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide", "percent", "abs_diff",
        "help", "history", "clear", "undo", "redo", "save", "load", "exit",
    ]

    # Each command should appear in help output
    for command in commands:
        assert command in output


def test_calculation_command():
    """Verify CalculationCommand executes calculator operations correctly."""
    calculator = Mock()

    # Mock calculator operation result
    calculator.perform_operation.return_value = 10

    cmd = CalculationCommand(calculator, "add", 5, 5)
    result = cmd.execute()

    # Validate returned result and method calls
    assert result == 10
    calculator.set_operation.assert_called_once()
    calculator.perform_operation.assert_called_once_with(5, 5)


def test_create_unregistered_item_raises(calculator):
    """Ensure factory raises error for unknown commands."""
    with pytest.raises(ValueError, match="Unregistered item: unknown"):
        ReplCommandFactory.create("unknown", calculator=calculator)


def test_exception_save(calculator, caplog):
    """Ensure SaveCommand logs errors when save fails."""
    with caplog.at_level(logging.INFO):

        # Simulate failure during save
        with patch(
            "app.calculator.Calculator.save_history",
            side_effect=Exception("Simulated Error")
        ):
            with pytest.raises(Exception):
                SaveCommand(calculator).execute()

        # Verify error message was logged
        assert "Error: " in caplog.text


def test_exception_load(calculator, caplog):
    """Ensure LoadCommand logs errors when load fails."""
    with caplog.at_level(logging.INFO):

        # Simulate failure during load
        with patch(
            "app.calculator.Calculator.load_history",
            side_effect=Exception("Simulated Error")
        ):
            with pytest.raises(Exception):
                LoadCommand(calculator).execute()

        # Verify error message was logged
        assert "Error: " in caplog.text

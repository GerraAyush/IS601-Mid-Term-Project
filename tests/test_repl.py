# Python Modules
import pytest
from unittest.mock import patch

# App Imports
from app.calculator_repl import calculator_repl, print_operations

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

@pytest.mark.parametrize("cmd", ["undo", "redo", "save", "load"])
def test_repl_not_implemented_commands(cmd, capsys):
    inputs = iter([cmd, "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "Not implemented" in captured.out

def test_repl_invalid_operation(capsys):
    inputs = iter(["invalid_cmd", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "Invalid operation: invalid_cmd" in captured.out

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

def test_repl_invalid_operand():
    inputs = iter([
        "add",
        "abc",  # invalid operand triggers ValueError
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         pytest.raises(ValueError, match="Invalid operand value"):
        calculator_repl()

def test_repl_exit(capsys):
    inputs = iter(["exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        with pytest.raises(SystemExit):
            calculator_repl()

    captured = capsys.readouterr()
    assert "GoodBye! Exiting" in captured.out
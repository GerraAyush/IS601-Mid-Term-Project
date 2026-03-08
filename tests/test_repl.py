# Python Modules
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# App Imports
from app.operation import Addition
from app.exceptions import OperationError, ValidationError
from app.calculator_repl import CalculatorRepl, calculator_repl
from app.exceptions import ExitSignal


def test_repl_help_then_exit(calculator):
    """REPL executes 'help' command and exits cleanly."""
    inputs = iter(["help", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_repl_history_then_exit(calculator):
    """REPL shows history and exits cleanly."""
    inputs = iter(["history", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_repl_clear_then_exit(calculator, capsys):
    """REPL clears history and prints confirmation."""
    inputs = iter(["clear", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()

    captured = capsys.readouterr()
    assert "Cleared history." in captured.out


def test_clear_history_clears_stacks(calculator):
    """Clearing history empties undo/redo stacks and history."""
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[2, 3]):
        calculator.perform_operation(2, 3)
        assert len(calculator.undo_stack) == 1
        calculator.clear_history()
        assert calculator.history == []
        assert calculator.undo_stack == []
        assert calculator.redo_stack == []


def test_repl_invalid_operation(calculator, capsys):
    """REPL prints error message for unknown commands."""
    inputs = iter(["invalid_cmd", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()

    captured = capsys.readouterr()
    assert "Unknown command: 'invalid_cmd'. Type 'help' for available commands." in captured.out


def test_repl_valid_operation_add(capsys):
    """REPL executes valid add operation and displays result."""
    inputs = iter(["add", "2", "3", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit):
        calculator_repl()

    captured = capsys.readouterr()
    assert "Result: 5" in captured.out


def test_repl_undo_successful(calculator, capsys):
    """REPL undoes last operation successfully."""
    inputs = iter(["add", "2", "3", "undo", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "Undo successful!" in captured.out


def test_repl_no_undo(calculator, capsys):
    """REPL informs user when undo stack is empty."""
    inputs = iter(["undo", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "Nothing to undo" in captured.out


def test_repl_redo_successful(calculator, capsys):
    """REPL redoes previously undone operation."""
    inputs = iter(["add", "2", "3", "undo", "redo", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "Redo successful!" in captured.out


def test_repl_no_redo(calculator, capsys):
    """REPL informs user when redo stack is empty."""
    inputs = iter(["redo", "exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "Nothing to redo" in captured.out


def test_undo_empty_stack(calculator):
    """Undo returns False when undo stack is empty."""
    assert calculator.undo() is False


def test_redo_empty_stack(calculator):
    """Redo returns False when redo stack is empty."""
    assert calculator.redo() is False


def test_undo_modifies_history(calculator):
    """Undo removes last calculation from history."""
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2]):
        calculator.perform_operation(1, 2)
        assert len(calculator.history) == 1
        assert calculator.undo() is True
        assert calculator.history == []


def test_redo_restores_history(calculator):
    """Redo restores calculation to history."""
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2]):
        calculator.perform_operation(1, 2)
        calculator.undo()
        assert calculator.history == []
        assert calculator.redo() is True
        assert len(calculator.history) == 1


def test_repl_exit(calculator, capsys):
    """REPL exits cleanly with goodbye message."""
    inputs = iter(["exit"])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()

    captured = capsys.readouterr()
    assert "GoodBye! Exiting" in captured.out


def test_repl_save_successful(calculator, capsys):
    """REPL saves history successfully after a calculation."""
    inputs = iter([
        "add",
        "2",
        "3",
        "save",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "History saved successfully" in captured.out


def test_repl_load_successful(calculator, capsys):
    """REPL loads history successfully after save."""
    inputs = iter([
        "add",
        "2",
        "3",
        "save",
        "load",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()
    
    captured = capsys.readouterr()
    assert "History loaded successfully" in captured.out


def test_perform_operation_without_setting_operation(calculator):
    """Raises OperationError if no operation is set."""
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(1, 2)


def test_perform_operation_validation_error_passthrough(calculator):
    """ValidationError is propagated from InputValidator."""
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=ValidationError("Invalid input")):
        with pytest.raises(ValidationError):
            calculator.perform_operation("bad", 2)


def test_perform_operation_wraps_generic_exception(calculator):
    """Generic exception during execution is wrapped in OperationError."""
    calculator.set_operation(Addition(cmd="add"))

    with patch("app.calculator.InputValidator.validate_number", side_effect=[1, 2]), \
         patch.object(Addition, "execute", side_effect=Exception("boom")):
        with pytest.raises(OperationError, match="Operation failed: boom"):
            calculator.perform_operation(1, 2)


def test_save_history_exception(calculator):
    """Raises OperationError if saving history fails."""
    with patch("pandas.DataFrame.to_csv", side_effect=Exception("fail")):
        with pytest.raises(OperationError):
            calculator.save_history()


def test_load_history_exception(calculator):
    """Raises OperationError if loading history fails."""
    calculator.save_history()

    with patch("pandas.read_csv", side_effect=Exception("fail")):
        with pytest.raises(OperationError):
            calculator.load_history()


def test_exit_command(calculator):
    """REPL handles 'exit' command and terminates cleanly."""
    with patch("builtins.input", side_effect=["exit"]), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_keyboard_interrupt(calculator):
    """REPL handles KeyboardInterrupt gracefully."""
    with patch("builtins.input", side_effect=[KeyboardInterrupt, "exit"]), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_eof_error(calculator):
    """REPL handles EOFError gracefully (e.g., Ctrl+D)."""
    with patch("builtins.input", side_effect=EOFError), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_invalid_operand(calculator):
    """REPL handles invalid operand input and continues execution."""
    inputs = iter([
        "add",
        "abc",     # invalid operand
        "exit"
    ])

    with patch("builtins.input", side_effect=inputs), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


@patch("app.calculator_repl.CalculatorRepl")
@patch("app.calculator_repl.CommandInvoker")
@patch("app.calculator_repl.ReplCommandFactory")
@patch("app.calculator_repl.AutoSaveObserver")
@patch("app.calculator_repl.LoggingObserver")
@patch("app.calculator_repl.Calculator")
@patch("app.calculator_repl.CalculatorConfig")
@patch("app.calculator_repl.get_project_root")
def test_calculator_repl_auto_save_branch(
    mock_get_root,
    mock_config_cls,
    mock_calc_cls,
    mock_logging_observer,
    mock_autosave_observer,
    mock_factory,
    mock_invoker_cls,
    mock_repl_cls,
):
    """Test the auto-save branch of calculator_repl sets up observers and save commands."""
    mock_get_root.return_value = Path(".")
    mock_config = MagicMock()
    mock_config.auto_save = True
    mock_config_cls.return_value = mock_config

    mock_calculator = MagicMock()
    mock_calculator.config = mock_config
    mock_calc_cls.return_value = mock_calculator

    mock_invoker = MagicMock()
    mock_invoker_cls.return_value = mock_invoker

    mock_factory.create.return_value = MagicMock()

    calculator_repl()

    # Ensure 'save' command was created with auto-save observer
    mock_factory.create.assert_any_call("save", calculator=mock_calculator)
    mock_invoker.set_on_finish.assert_called()


def test_start_command_output(monkeypatch, calculator, invoker):
    """Test that the REPL runs start command and output is captured."""
    repl = CalculatorRepl(calculator, invoker)

    monkeypatch.setattr(invoker, "run_start", lambda: "HELLO")

    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    repl.start()


def test_exit_signal(monkeypatch, calculator, invoker):
    """REPL properly exits when ExitSignal is raised."""
    repl = CalculatorRepl(calculator, invoker)

    def fake_execute(command):
        raise ExitSignal()

    monkeypatch.setattr(invoker, "execute", fake_execute)
    monkeypatch.setattr(invoker, "run_finish", lambda: "Saved")

    inputs = iter(["exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    repl.start()


def test_repl_config_set(calculator, invoker):
    """Ensure REPL correctly stores the passed ReplConfig."""
    from app.config import ReplConfig
    repl_config = ReplConfig()
    repl = CalculatorRepl(calculator, invoker, repl_config)
    assert repl.config is repl_config


def test_setup_colorama_calls_setup():
    """Test that REPL setup calls colorama/console setup for text color."""
    calculator = MagicMock()
    invoker = MagicMock()
    mock_console = MagicMock()
    mock_console.initiated = False

    with patch("app.calculator_repl.Console", return_value=mock_console):
        repl = CalculatorRepl(calculator, invoker)

    mock_console.setup.assert_called_once_with(repl.config.color_text)


def test_repl_ignores_escape_sequence(calculator):
    """REPL ignores escape sequences in input (like arrow keys)."""
    inputs = iter([
        "\x1b[A",  # becomes "" after regex -> continue
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()


def test_repl_ignores_operand_escape_sequence(calculator):
    """REPL ignores escape sequences entered as operands."""
    inputs = iter([
        "add",
        "\x1b[A",  # becomes "" after regex -> continue
        "1",
        "2",
        "exit"
    ])

    with patch("builtins.input", side_effect=lambda _: next(inputs)), \
         patch("sys.exit", side_effect=SystemExit), \
         patch("app.calculator_repl.Calculator", return_value=calculator):
        calculator_repl()

# Python modules
import pytest
from unittest.mock import MagicMock

# App Imports
from app.command_invoker import CommandInvoker
from app.command import Command, ExitCommand


def test_set_on_start_and_run():
    """Verify that a start command is executed when run_start is called."""
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=Command)

    # Set the start command
    invoker.set_on_start(mock_command)
    # Execute start
    invoker.run_start()

    # Assert the mock command's execute was called once
    mock_command.execute.assert_called_once()


def test_run_start_when_none():
    """Ensure run_start does nothing if no start command is set."""
    invoker = CommandInvoker()
    invoker.run_start()  # Should not raise or perform anything


def test_exit_set_on_finish():
    """Ensure setting an ExitCommand as finish raises TypeError."""
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=ExitCommand)

    with pytest.raises(TypeError, match="Finish command cannot be ExitCommand"):
        invoker.set_on_finish(mock_command)


def test_set_on_finish_and_run():
    """Verify that a finish command is executed when run_finish is called."""
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=Command)

    # Set the finish command
    invoker.set_on_finish(mock_command)
    # Execute finish
    invoker.run_finish()

    # Assert the mock command's execute was called once
    mock_command.execute.assert_called_once()


def test_run_finish_when_none():
    """Ensure run_finish does nothing if no finish command is set."""
    invoker = CommandInvoker()
    invoker.run_finish()  # Should not raise or perform anything


def test_execute_invalid_type():
    """Ensure executing a non-Command object raises TypeError."""
    invoker = CommandInvoker()

    with pytest.raises(TypeError):
        invoker.execute("not a command")

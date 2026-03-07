import pytest
from unittest.mock import MagicMock
from app.command_invoker import CommandInvoker
from app.command import Command, ExitCommand


def test_set_on_start_and_run():
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=Command)

    invoker.set_on_start(mock_command)
    invoker.run_start()

    mock_command.execute.assert_called_once()


def test_run_start_when_none():
    invoker = CommandInvoker()
    invoker.run_start()  # should do nothing


def test_exit_set_on_finish():
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=ExitCommand)

    with pytest.raises(TypeError, match="Finish command cannot be ExitCommand"):
        invoker.set_on_finish(mock_command)


def test_set_on_finish_and_run():
    invoker = CommandInvoker()
    mock_command = MagicMock(spec=Command)

    invoker.set_on_finish(mock_command)
    invoker.run_finish()

    mock_command.execute.assert_called_once()


def test_run_finish_when_none():
    invoker = CommandInvoker()
    invoker.run_finish()  # should do nothing


def test_execute_invalid_type():
    invoker = CommandInvoker()

    with pytest.raises(TypeError):
        invoker.execute("not a command")
    
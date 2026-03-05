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


def test_execute_command_with_result(capsys):
    invoker = CommandInvoker()

    mock_command = MagicMock(spec=Command)
    mock_command.execute.return_value = 42

    invoker.execute(mock_command)

    captured = capsys.readouterr()
    assert "Result: 42" in captured.out


def test_execute_command_without_result(capsys):
    invoker = CommandInvoker()

    mock_command = MagicMock(spec=Command)
    mock_command.execute.return_value = None

    invoker.execute(mock_command)

    captured = capsys.readouterr()
    assert captured.out == ""


def test_execute_exit_command():
    invoker = CommandInvoker()

    mock_exit = MagicMock(spec=ExitCommand)
    mock_finish = MagicMock(spec=Command)

    invoker.set_on_finish(mock_finish)

    invoker.execute(mock_exit)

    mock_exit.execute.assert_any_call(on_exit_command=mock_finish)
    
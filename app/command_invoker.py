# Python Modules
from typing import Optional

# App Imports
from app.datatypes import Number
from app.command import Command, ExitCommand


class CommandInvoker:
    """
    Invoker component of the Command pattern.

    This class is responsible for executing command objects and managing
    optional lifecycle hooks. It can execute commands directly as well as
    run predefined commands during application startup and shutdown.

    The invoker does not contain business logic for commands; it simply
    delegates execution to the command objects.
    """

    def __init__(self):
        """
        Initialize the command invoker.

        Two optional lifecycle commands may be configured:
        - `_on_start`: executed when the application starts.
        - `_on_finish`: executed when the application finishes.
        """

        # Command executed when the application starts
        self._on_start: Command | None = None

        # Command executed when the application finishes
        self._on_finish: Command | None = None

    def set_on_start(self, command: Command) -> None:
        """
        Register a command to run when the application starts.

        Parameters
        ----------
        command : Command
            Command instance to execute during startup.
        """
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        """
        Register a command to run when the application finishes.

        The finish command cannot be an ExitCommand, since exit control
        is handled separately by the REPL.

        Parameters
        ----------
        command : Command
            Command instance to execute during shutdown.

        Raises
        ------
        TypeError
            If the provided command is an ExitCommand.
        """
        if isinstance(command, ExitCommand):
            raise TypeError("Finish command cannot be ExitCommand")

        self._on_finish = command

    def execute(self, command: Command) -> Optional[str | Number]:
        """
        Execute a command.

        The invoker simply delegates execution to the provided command.

        Parameters
        ----------
        command : Command
            Command instance to execute.

        Returns
        -------
        Optional[str | Number]
            Result returned by the command, if any.

        Raises
        ------
        TypeError
            If the provided object is not a Command instance.
        """
        if not isinstance(command, Command):
            raise TypeError("Only Command instances can be executed")

        return command.execute()

    def run_start(self) -> Optional[str | Number]:
        """
        Execute the registered startup command.

        Returns
        -------
        Optional[str | Number]
            Result returned by the startup command, or None if no
            startup command is configured.
        """
        if self._on_start:
            return self._on_start.execute()

    def run_finish(self) -> Optional[str | Number]:
        """
        Execute the registered shutdown command.

        Returns
        -------
        Optional[str | Number]
            Result returned by the shutdown command, or None if no
            finish command is configured.
        """
        if self._on_finish:
            return self._on_finish.execute()

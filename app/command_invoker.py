# App Imports
from app.command import Command, ExitCommand


class CommandInvoker:
    """
    Invoker class for the Command pattern.

    Responsibilities:
    - Store and run "start" and "finish" commands.
    - Execute any command passed to it, including ExitCommand with finish hook.
    - Provide a central point to manage command execution lifecycle.
    """

    def __init__(self):
        """
        Initialize the invoker with optional start and finish commands.
        """
        # Command to execute at the start of an operation
        self._on_start: Command | None = None

        # Command to execute at the end of an operation (e.g., on exit)
        self._on_finish: Command | None = None

    def set_on_start(self, command: Command) -> None:
        """
        Set a command to execute when starting an operation.

        Parameters
        ----------
        command : Command
            The command to execute at start.
        """
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        """
        Set a command to execute when finishing an operation.

        Parameters
        ----------
        command : Command
            The command to execute at finish.
        """
        self._on_finish = command

    def execute(self, command: Command) -> None:
        """
        Execute a given command.

        If the command is an ExitCommand, it will first execute the finish
        command (_on_finish) if defined, before executing itself.

        Parameters
        ----------
        command : Command
            The command to execute.

        Raises
        ------
        TypeError
            If the passed object is not a Command instance.
        """
        if not isinstance(command, Command):
            raise TypeError("Only Command instances can be executed")
        
        # Handle ExitCommand specially by running finish command first
        if isinstance(command, ExitCommand):
            command.execute(on_exit_command=self._on_finish)

        # Execute the command normally
        result = command.execute()
        if result is not None:
            print(f"Result: {result}")

    def run_start(self) -> None:
        """
        Execute the start command if it exists.
        """
        if self._on_start:
            self._on_start.execute()

    def run_finish(self) -> None:
        """
        Execute the finish command if it exists.
        """
        if self._on_finish:
            self._on_finish.execute()

# App Imports
from app.command import Command, ExitCommand


class CommandInvoker:

    def __init__(self):
        self._on_start: Command | None = None
        self._on_finish: Command | None = None

    def set_on_start(self, command: Command) -> None:
        self._on_start = command

    def set_on_finish(self, command: Command) -> None:
        self._on_finish = command

    def execute(self, command: Command) -> None:
        if not isinstance(command, Command):
            raise TypeError("Only Command instances can be executed")
        
        if isinstance(command, ExitCommand):
            command.execute(on_exit_command=self._on_finish)

        result = command.execute()
        if result is not None:
            print(f"Result: {result}")

    def run_start(self) -> None:
        if self._on_start:
            self._on_start.execute()

    def run_finish(self) -> None:
        if self._on_finish:
            self._on_finish.execute()

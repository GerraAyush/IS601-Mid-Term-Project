# Python Modules
import logging

# Datatypes
from typing import Union
from abc import ABC, abstractmethod

# App imports
from app.datatypes import Number
from app.factory import FactoryBase
from app.operation import OperationFactory
from app.registry import command
from app.exceptions import ExitSignal


class Command(ABC):
    """
    Abstract base class for all commands.

    Concrete command classes must implement the `execute` method.
    Commands encapsulate an action that can be executed by the
    command invoker within the REPL.
    """

    @abstractmethod
    def execute(self) -> Union[str, Number, None]:
        """
        Execute the command.

        Returns
        -------
        Union[str, Number, None]
            Result produced by the command. Many commands return a
            message string, calculation commands return a numeric
            result, and some commands may return None.
        """
        pass  # pragma: no cover


class CalculationCommand(Command):
    """
    Command responsible for executing a mathematical operation.

    This command delegates the actual computation to the Calculator
    instance by creating the requested operation via the
    OperationFactory and executing it with the provided operands.

    Parameters
    ----------
    calculator : Calculator
        Calculator instance used to perform the operation.
    operation_name : str
        Name of the operation to execute (e.g., 'add', 'subtract').
    operand1 : Number
        First operand.
    operand2 : Number
        Second operand.
    """

    def __init__(self, calculator: "Calculator", operation_name: str, operand1: Number, operand2: Number):
        self.calculator = calculator
        self.operation_name = operation_name
        self.a = operand1
        self.b = operand2

    def execute(self) -> Number:
        """
        Execute the calculation command.

        The operation is created using the OperationFactory and then
        executed by the calculator instance.

        Returns
        -------
        Number
            Result of the mathematical operation.
        """
        operation = OperationFactory.create(self.operation_name)
        self.calculator.set_operation(operation)
        return self.calculator.perform_operation(self.a, self.b)


class ReplCommandFactory(FactoryBase):
    """
    Factory responsible for creating REPL command instances.

    Command classes decorated with the `@command` decorator are
    automatically registered in this factory. The factory allows
    commands to be created dynamically based on their registered
    name.
    """

    _item_dict = {}
    _base_class = Command


@command(name="help", description="Show all available operations")
class HelpCommand(Command):
    """
    Command that displays all available calculator operations
    and REPL commands.
    """

    def execute(self) -> str:
        return (
            "Available commands:\n"
            + OperationFactory.list_items()
            + ReplCommandFactory.list_items()
        )


@command(name="history", description="Show calculation history")
class HistoryCommand(Command):
    """
    Command that displays the calculator's stored history.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Retrieve and return the calculation history.

        Returns
        -------
        str
            Formatted history output.
        """
        return self.calculator.show_history()


@command(name="clear", description="Clear calculation history")
class ClearCommand(Command):
    """
    Command that clears all stored calculation history.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Clear the calculator history.

        Returns
        -------
        str
            Confirmation message.
        """
        self.calculator.clear_history()
        return "Cleared history."


@command(name="undo", description="Undo the last calculation")
class UndoCommand(Command):
    """
    Command that undoes the most recent calculation.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Undo the most recent calculation.

        Returns
        -------
        str
            Result message indicating whether the operation succeeded.
        """
        return "Undo successful!" if self.calculator.undo() else "Nothing to undo"


@command(name="redo", description="Redo the last undone calculation")
class RedoCommand(Command):
    """
    Command that re-applies the most recently undone calculation.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Redo the last undone calculation.

        Returns
        -------
        str
            Result message indicating whether the operation succeeded.
        """
        return "Redo successful!" if self.calculator.redo() else "Nothing to redo"


@command(name="save", description="Save calculation history to file")
class SaveCommand(Command):
    """
    Command that persists the calculator history to disk.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Save the current calculation history.

        Returns
        -------
        str
            Confirmation message if the save succeeds.

        Raises
        ------
        Exception
            Propagates any errors encountered during saving.
        """
        try:
            self.calculator.save_history()
            return "History saved successfully"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise


@command(name="load", description="Load calculation history from file")
class LoadCommand(Command):
    """
    Command that loads previously saved calculation history.
    """

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> str:
        """
        Load calculation history from storage.

        Returns
        -------
        str
            Confirmation message if loading succeeds.

        Raises
        ------
        Exception
            Propagates any errors encountered during loading.
        """
        try:
            self.calculator.load_history()
            return "History loaded successfully"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise


@command(name="exit", description="Exit the calculator")
class ExitCommand(Command):
    """
    Command that signals the REPL to terminate.

    Instead of directly terminating the program, this command raises
    an ExitSignal exception. The REPL is responsible for catching the
    signal and performing any necessary cleanup before exiting.
    """

    def execute(self) -> None:
        """
        Raise an ExitSignal to terminate the REPL loop.
        """
        raise ExitSignal()
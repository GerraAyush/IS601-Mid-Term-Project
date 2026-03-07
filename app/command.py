# Python Modules
import sys

# Datatypes
from typing import Union, Optional
from abc import ABC, abstractmethod

# App imports
from app.datatypes import Number
from app.factory import FactoryBase
from app.operation import OperationFactory

class Command(ABC):
    """
    Abstract base class for all commands.

    All commands should implement the `execute` method.
    """
    @abstractmethod
    def execute(self) -> Union[Number, None]:
        """
        Execute the command.

        Returns
        -------
        Union[Number, None]
            The result of the command if applicable, else None.
        """
        pass    # pragma: no cover

class CalculationCommand(Command):
    """
    Command to perform a calculation using the Calculator.

    Parameters
    ----------
    calculator : Calculator
        Calculator instance to perform operations on.
    operation_name : str
        Name of the operation to perform (e.g., 'add', 'subtract').
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
        Perform the calculation by creating the operation
        and executing it via the Calculator instance.

        Returns
        -------
        Number
            Result of the operation.
        """
        operation = OperationFactory.create(self.operation_name)
        self.calculator.set_operation(operation)
        return self.calculator.perform_operation(self.a, self.b)

class HistoryCommand(Command):
    """Command to display the calculation history."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        self.calculator.show_history()


class ClearCommand(Command):
    """Command to clear the calculation history."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        self.calculator.clear_history()
        print("Cleared history.")


class UndoCommand(Command):
    """Command to undo the last calculation."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        if self.calculator.undo():
            print("Undo successful!")
        else:
            print("Nothing to undo")


class RedoCommand(Command):
    """Command to redo the last undone calculation."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        if self.calculator.redo():
            print("Redo successful!")
        else:
            print("Nothing to redo")


class SaveCommand(Command):
    """Command to save calculation history to a file."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        try:
            self.calculator.save_history()
            print("History saved successfully")
        except Exception as e:
            print(f"Error saving history: {e}")


class LoadCommand(Command):
    """Command to load calculation history from a file."""

    def __init__(self, calculator: "Calculator"):
        self.calculator = calculator

    def execute(self) -> None:
        try:
            self.calculator.load_history()
            print("History loaded successfully")
        except Exception as e:
            print(f"Error loading history: {e}")


class ExitCommand(Command):
    """
    Command to exit the calculator REPL.

    Parameters
    ----------
    on_exit_command : Optional[Command], default=None
        Command to execute before exiting (e.g., save command).
    """

    def execute(self, on_exit_command: Optional[Command] = None) -> None:

        if on_exit_command:
            if not issubclass(type(on_exit_command), Command):
                raise TypeError(f"Item class must inherit from Command")
            
            if isinstance(on_exit_command, ExitCommand):
                raise TypeError(f"Item cannot be ExitCommand")

            result = on_exit_command.execute()
            if result:
                print(f"Result: {result}")

        print("\nGoodBye! Exiting ...\n")
        sys.exit()

class ReplCommandFactory(FactoryBase):
    """
    Factory to create REPL commands dynamically.

    Registers commands like help, history, undo, redo, save, load, and exit.
    """
    _item_dict = {
        'help' : {
            '_cls' : HelpCommand,
            'desc' : 'Show all available operations'
        },
        'history' : {
            '_cls' : HistoryCommand,
            'desc' : 'Show calculation history',
        },
        'clear' : {
            '_cls' : ClearCommand,
            'desc' : 'Clear calculation history',
        },
        'undo' : {
            '_cls' : UndoCommand,
            'desc' : 'Undo the last calculation',
        },
        'redo' : {
            '_cls' : RedoCommand,
            'desc' : 'Redo the last undone calculation',
        },
        'save' : {
            '_cls' : SaveCommand,
            'desc' : 'Save calculation history to file',
        },
        'load' : {
            '_cls' : LoadCommand,
            'desc' : 'Load calculation history from file',
        },
        'exit' : {
            '_cls' : ExitCommand,
            'desc' : 'Exit the calculator',
        }
    }
    _base_class = Command

# Python Modules
import logging

# Datatypes
from typing import List

# App Imports
from app.calculator import Calculator
from app.operation import OperationFactory
from app.calculator_config import CalculatorConfig
from app.command import Command, CalculationCommand, ReplCommandFactory
from app.history import LoggingObserver, AutoSaveObserver
from app.exceptions import ValidationError, OperationError
from app.utils import get_project_root
from app.command_invoker import CommandInvoker
from app.datatypes import Number


class CalculatorRepl:

    def __init__(self, calculator: Calculator, invoker: CommandInvoker):
        self.calculator = calculator
        self.invoker = invoker

    def start(self) -> None:
        print("Welcome! I will help with Math. Dumbo.")

        self.invoker.run_start()

        while True:
            try:
                user_command : str = input("\nEnter the operation you want to perform: ").strip()

                if ReplCommandFactory.is_registered(user_command):
                    if user_command in ["help", "exit"]:
                        command: Command = ReplCommandFactory.create(user_command)
                    else:
                        command: Command = ReplCommandFactory.create(user_command, calculator=self.calculator)
                    self.invoker.execute(command)
                    continue

                if OperationFactory.is_registered(user_command):
                    operands: List[Number] = self._get_operands()
                    command: Command = CalculationCommand(
                        calculator=self.calculator, 
                        operation_name=user_command, 
                        operand1=operands[0],
                        operand2=operands[1]
                    )
                    self.invoker.execute(command)
                    continue

                print(f"Unknown command: '{user_command}'. Type 'help' for available commands.")

            except (ValidationError, OperationError) as e:
                print(f"Error: {e}")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                logging.info("Operation cancelled")

            except EOFError:
                print("\nInput terminated. Exiting...")
                logging.info("Input terminated. Exiting...")
                break

        self.invoker.run_finish()

    def _get_operands(self) -> None:
        operands: List[Number] = []
        while len(operands) != 2:
            try:
                user_input = input(f"Enter operand#{len(operands) + 1}: ").strip()
                operands.append(float(user_input) if '.' in user_input else int(user_input))
            except :
                raise OperationError(f"Invalid operand value: {user_input}")
        return operands


def calculator_repl() -> None:
    config = CalculatorConfig(base_dir=get_project_root())
    calculator = Calculator(config)

    calculator.add_observer(LoggingObserver())
    calculator.add_observer(AutoSaveObserver(calculator))

    invoker = CommandInvoker()
    invoker.set_on_start(ReplCommandFactory.create("help"))
    if calculator.config.auto_save:
        invoker.set_on_finish(ReplCommandFactory.create("save", calculator=calculator))

    repl = CalculatorRepl(calculator, invoker)
    repl.start()

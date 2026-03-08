# Python Modules
import re
import logging

# Datatypes
from typing import List, Optional

# App Imports
from app.datatypes import Number
from app.calculator import Calculator
from app.operation import OperationFactory
from app.config import CalculatorConfig, ReplConfig
from app.command import Command, CalculationCommand, ReplCommandFactory
from app.history import LoggingObserver, AutoSaveObserver
from app.exceptions import ValidationError, OperationError, ExitSignal
from app.command_invoker import CommandInvoker
from app.utils import get_project_root
from app.console import Console


class CalculatorRepl:
    """
    Interactive Read-Eval-Print Loop (REPL) interface for the calculator.

    This class continuously reads user input from the terminal, interprets
    the command, executes the appropriate calculator operation or command,
    and prints the result. It integrates the Command pattern and Factory
    pattern to dynamically create and execute commands.
    """

    def __init__(
            self, 
            calculator: Calculator, 
            invoker: CommandInvoker, 
            config: Optional[ReplConfig] = None
        ):
        """
        Initialize the REPL with a calculator instance and a command invoker.

        Parameters
        ----------
        calculator : Calculator
            The calculator instance used to perform operations and manage history.
        invoker : CommandInvoker
            The command invoker responsible for executing commands.
        """
        if config is None:
            config = ReplConfig()
        
        self.config = config
        self.config.validate()

        self.calculator = calculator
        self.invoker = invoker
        
        self._setup_colorama()

    def _setup_colorama(self) -> None:
        """
        Initialize color support for the terminal.
        """
        self.console = Console()
        if not self.console.initiated:
            self.console.setup(self.config.color_text)

    def start(self) -> None:
        """
        Start the calculator REPL loop.

        The method continuously accepts user commands until the user exits.
        Commands are interpreted using registered command factories and
        operation factories.
        """
        print("Welcome! I will help with Math. Dumbo.")

        # Execute any startup command (e.g., display help menu)
        result = self.invoker.run_start()

        # Print the result
        if result is not None:
            self.console.info(result)

        while True:
            try:
                # Read user command and remove surrounding whitespace
                user_command : str = input("\nEnter the operation you want to perform: ").strip()

                # Ignore arrow keys / terminal control sequences
                user_command = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', user_command)
                if not user_command:
                    continue

                result: Optional[str | Number] = None

                # Check if the command is a registered REPL command
                if ReplCommandFactory.is_registered(user_command):

                    # Some commands do not require calculator injection
                    if user_command in ["help", "exit"]:
                        command: Command = ReplCommandFactory.create(user_command)
                    else:
                        # Commands like save/load require calculator preference
                        command: Command = ReplCommandFactory.create(user_command, calculator=self.calculator)

                    # Execute the command using the invoker
                    try:
                        result = self.invoker.execute(command)
                    
                    except ExitSignal:
                        result = self.invoker.run_finish()
                        if result is not None:
                            self.console.success(result)
                        self.console.info("\nGoodBye! Exiting ...\n")
                        break

                    self.console.success(result)
                    
                # Check if the command corresponds to a mathematical operation
                elif OperationFactory.is_registered(user_command):

                    # Collect two operands from the user
                    operands: List[Number] = self._get_operands()
                    
                    # Create a calculation command to perform the operation
                    command: Command = CalculationCommand(
                        calculator=self.calculator,
                        operation_name=user_command,
                        operand1=operands[0],
                        operand2=operands[1]
                    )

                    # Execute the calculation command
                    result = self.invoker.execute(command)

                    # Print the result
                    self.console.success(f"Result: {result}")

                else:
                    # If command is not recognized
                    self.console.warning(f"Unknown command: '{user_command}'. Type 'help' for available commands.")

            # Handle validation and operation errors
            except (ValidationError, OperationError) as e:
                self.console.error(f"Error: {e}")

            # Handle user interruption (Ctrl+C)
            except KeyboardInterrupt:
                self.console.error("\nOperation cancelled")
                logging.info("Operation cancelled")

            # Handle input termination (Ctrl+D / EOF)
            except EOFError:
                self.console.error("\nInput terminated. Exiting...")
                logging.info("Input terminated. Exiting...")
                break


    def _get_operands(self) -> None:
        """
        Prompt the user to input two operands.

        Returns
        -------
        List[Number]
            A list containing two numeric operands entered by the user.

        Raises
        ------
        OperationError
            If the user enters an invalid numeric value.
        """
        operands: List[Number] = []

        # Continue asking until two operands are provided
        while len(operands) != 2:
            try:
                user_input = input(f"Enter operand#{len(operands) + 1}: ").strip()

                user_input = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', user_input)
                if not user_input:
                    continue
                
                # Convert input to float if it contains a decimal point,
                # otherwise convert to integer
                operands.append(float(user_input) if '.' in user_input else int(user_input))
            except ValueError as e:
                raise OperationError(f"Invalid operand value: {user_input}")
        return operands


def calculator_repl() -> None:
    """
    Entry point for starting the calculator REPL application.

    This function initializes the configuration, calculator instance,
    observers, and command invoker before starting the interactive REPL.
    """

    # Load configuration using project root as base directory
    config = CalculatorConfig(base_dir=get_project_root())

    # Create calculator instance
    calculator = Calculator(config)

    # Attach observers for logging and auto-saving history
    calculator.add_observer(LoggingObserver())
    calculator.add_observer(AutoSaveObserver(calculator))

    # Create command invoker responsible for executing commands
    invoker = CommandInvoker()
    
    # Run the help command when the application starts
    invoker.set_on_start(ReplCommandFactory.create("help"))

    # Automatically save history when the application exits
    if calculator.config.auto_save:
        invoker.set_on_finish(ReplCommandFactory.create("save", calculator=calculator))

    # Start the REPL interface
    repl = CalculatorRepl(calculator, invoker)
    repl.start()

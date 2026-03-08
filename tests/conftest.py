# Python Modules
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, PropertyMock, MagicMock

# App Imports
from app.operation import Addition
from app.calculator import Calculator
from app.command_invoker import CommandInvoker
from app.calculator_repl import CalculatorRepl
from app.config import CalculatorConfig


class FakeOperation:
    """
    Lightweight fake operation used for testing.

    This class mimics the behavior of a calculator operation but avoids
    using the real operation classes. It allows tests to verify command
    execution and calculator integration without depending on the
    actual operation implementations or factory registrations.
    """

    def __init__(self, name="add"):
        """
        Initialize the fake operation.

        Parameters
        ----------
        name : str
            Name of the operation (used mainly for display/debugging).
        """
        self.name = name

    def execute(self, a, b):
        """
        Simulate performing an operation.

        Parameters
        ----------
        a : Number
            First operand
        b : Number
            Second operand

        Returns
        -------
        Number
            The sum of the two operands.
        """
        return a + b

    def __str__(self):
        """
        Return the operation name.

        This allows the fake operation to behave similarly to real
        operations when converted to a string.
        """
        return self.name
    

@pytest.fixture
def calculator():
    """
    Provide a Calculator instance configured with a temporary filesystem.

    The calculator relies on configuration paths for logging and history.
    To avoid writing to the real filesystem during tests, this fixture:

    - Creates a temporary directory
    - Mocks configuration path properties
    - Returns a Calculator configured to use the temporary paths

    This ensures tests remain isolated and deterministic.
    """
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch configuration properties so that logs and history files
        # are written to the temporary directory instead of the real project
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            yield Calculator(config=config)


@pytest.fixture
def fake_operation():
    """
    Provide a reusable FakeOperation instance.

    This fixture is useful when testing calculator operations without
    relying on real operation implementations or factory registration.
    """
    return FakeOperation("Addition")


@pytest.fixture
def mock_factory(fake_operation):
    """
    Mock the OperationFactory.create method.

    This fixture replaces the factory's create method so that it always
    returns the provided fake operation. This allows tests to focus on
    command execution and calculator logic without depending on the
    real operation factory implementation.
    """
    with patch("app.calculation.OperationFactory.create") as mock:
        mock.return_value = fake_operation
        yield mock


@pytest.fixture
def addition_op():
    """
    Provide a real Addition operation instance.

    This fixture is useful when tests require a real operation instead
    of a mocked one, such as when validating calculator arithmetic logic.
    """
    return Addition(cmd="add")


@pytest.fixture
def invoker():
    """
    Provide a CommandInvoker instance.

    The CommandInvoker is responsible for executing command objects
    following the Command design pattern. Tests can use this fixture
    to verify command execution behavior.
    """
    return CommandInvoker()


@pytest.fixture
def repl(calculator, invoker):
    """
    Provide a CalculatorRepl instance with a mocked console.

    The console is mocked to prevent real terminal output during tests
    and to allow verification of printed messages (success, warning,
    error, etc.).

    Parameters
    ----------
    calculator : Calculator
        Calculator instance provided by the calculator fixture
    invoker : CommandInvoker
        Command invoker used by the REPL

    Returns
    -------
    CalculatorRepl
        REPL instance ready for testing
    """
    repl_instance = CalculatorRepl(calculator, invoker)

    # Replace console with a mock to capture output calls
    repl_instance.console = MagicMock()

    return repl_instance

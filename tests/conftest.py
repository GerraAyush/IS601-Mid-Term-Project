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
    def __init__(self, name="add"):
        self.name = name

    def execute(self, a, b):
        return a + b

    def __str__(self):
        return self.name
    

@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

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
    return FakeOperation("Addition")

@pytest.fixture
def mock_factory(fake_operation):
    with patch("app.calculation.OperationFactory.create") as mock:
        mock.return_value = fake_operation
        yield mock

@pytest.fixture
def addition_op():
    return Addition(cmd="add")

@pytest.fixture
def invoker():
    """Fixture for a CommandInvoker instance."""
    return CommandInvoker()

@pytest.fixture
def repl(calculator, invoker):
    """Fixture for a CalculatorRepl instance with mocked console."""
    repl_instance = CalculatorRepl(calculator, invoker)
    repl_instance.console = MagicMock()
    return repl_instance
    
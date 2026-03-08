# Python Modules
import pytest
from unittest.mock import Mock, patch

# App Imports
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.config import CalculatorConfig

# A sample calculation mock for use in tests
calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "addition"
calculation_mock.operand1 = 5
calculation_mock.operand2 = 3
calculation_mock.result = 8


@patch("app.history.logging.info")
def test_logging_observer_logs_calculation(logging_info_mock):
    """Ensure LoggingObserver logs the calculation correctly."""
    calculation_mock = Mock()
    calculation_mock.__str__ = Mock(return_value="Addition(5, 3) = 8")

    observer = LoggingObserver()
    observer.update(calculation_mock)

    logging_info_mock.assert_called_once_with(
        "Calculation performed: Addition(5, 3) = 8"
    )


def test_logging_observer_no_calculation():
    """Ensure LoggingObserver raises AttributeError when None is passed."""
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)


def test_autosave_observer_triggers_save():
    """Ensure AutoSaveObserver calls save_history when auto_save is enabled."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_called_once()


@patch('logging.info')
def test_autosave_observer_logs_autosave(logging_info_mock):
    """Ensure AutoSaveObserver logs the auto-save action."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with("History auto-saved")


def test_autosave_observer_does_not_trigger_save_when_disabled():
    """Ensure AutoSaveObserver does not call save_history if auto_save is False."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = False
    observer = AutoSaveObserver(calculator_mock)
    
    observer.update(calculation_mock)
    calculator_mock.save_history.assert_not_called()


def test_autosave_observer_invalid_calculator():
    """Ensure AutoSaveObserver raises TypeError if initialized with None."""
    with pytest.raises(TypeError):
        AutoSaveObserver(None)


def test_autosave_observer_no_calculation():
    """Ensure AutoSaveObserver raises AttributeError if None is passed as calculation."""
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    with pytest.raises(AttributeError):
        observer.update(None)

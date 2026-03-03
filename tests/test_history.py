# Python Modules
import pytest

# App Imports
from app.calculator import Calculator
from app.history import LoggingObserver, AutoSaveObserver


@pytest.fixture
def calculator(tmp_path):
    history_dir = tmp_path / "test_history"
    log_dir = tmp_path / "test_logs"

    history_dir.mkdir()
    log_dir.mkdir()

    history_file = history_dir / "calculator_history.csv"
    log_file = log_dir / "calculator_logs.log"

    return Calculator(history_dir=history_dir, history_file=history_file, log_dir=log_dir, log_file=log_file)

def test_logging_update_none():
    observer = LoggingObserver()
    with pytest.raises(AttributeError, match="Calculation cannot be None"):
        observer.update(None)

def test_autosave_update_none(calculator):
    observer = AutoSaveObserver(calculator)
    with pytest.raises(AttributeError, match="Calculation cannot be None"):
        observer.update(None)

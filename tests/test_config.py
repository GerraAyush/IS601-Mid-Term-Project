# Python Modules
import pytest
import os
from pathlib import Path

# Datatypes
from decimal import Decimal

# App imports
from app.config import CalculatorConfig
from app.exceptions import ConfigurationError


# Set environment variables used in tests
os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '500'
os.environ['CALCULATOR_PRECISION'] = '8'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'


def clear_env_vars(*args):
    """Helper function to remove specified environment variables."""
    for var in args:
        os.environ.pop(var, None)


def test_default_configuration():
    """Ensure configuration loads correctly from environment variables."""
    config = CalculatorConfig()

    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == 'utf-16'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()


def test_custom_configuration():
    """Verify custom constructor parameters override environment values."""
    config = CalculatorConfig(
        max_history_size=300,
        auto_save=True,
        precision=5,
        max_input_value=Decimal("500"),
        default_encoding="ascii"
    )

    assert config.max_history_size == 300
    assert config.auto_save is True
    assert config.precision == 5
    assert config.max_input_value == Decimal("500")
    assert config.default_encoding == "ascii"


def test_directory_properties():
    """Ensure directory properties use base_dir when env variables are absent."""
    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')

    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))

    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()


def test_file_properties():
    """Ensure file properties default correctly relative to base_dir."""
    clear_env_vars('CALCULATOR_HISTORY_FILE', 'CALCULATOR_LOG_FILE')

    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))

    assert config.history_file == Path('/custom_base_dir/history/calculator_history.csv').resolve()
    assert config.log_file == Path('/custom_base_dir/logs/calculator.log').resolve()


def test_invalid_max_history_size():
    """Ensure negative history size raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()


def test_invalid_precision():
    """Ensure invalid precision raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        config = CalculatorConfig(precision=-1)
        config.validate()


def test_invalid_max_input_value():
    """Ensure invalid max input value raises ConfigurationError."""
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        config = CalculatorConfig(max_input_value=Decimal("-1"))
        config.validate()


def test_auto_save_env_var_true():
    """Ensure 'true' environment value enables auto_save."""
    os.environ['CALCULATOR_AUTO_SAVE'] = 'true'

    config = CalculatorConfig(auto_save=None)

    assert config.auto_save is True


def test_auto_save_env_var_one():
    """Ensure '1' environment value enables auto_save."""
    os.environ['CALCULATOR_AUTO_SAVE'] = '1'

    config = CalculatorConfig(auto_save=None)

    assert config.auto_save is True


def test_auto_save_env_var_false():
    """Ensure 'false' environment value disables auto_save."""
    os.environ['CALCULATOR_AUTO_SAVE'] = 'false'

    config = CalculatorConfig(auto_save=None)

    assert config.auto_save is False


def test_auto_save_env_var_zero():
    """Ensure '0' environment value disables auto_save."""
    os.environ['CALCULATOR_AUTO_SAVE'] = '0'

    config = CalculatorConfig(auto_save=None)

    assert config.auto_save is False


def test_environment_overrides():
    """Ensure environment variables override default configuration."""
    config = CalculatorConfig()

    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == 'utf-16'


def test_default_fallbacks():
    """Ensure default values are used when environment variables are missing."""
    clear_env_vars(
        'CALCULATOR_MAX_HISTORY_SIZE',
        'CALCULATOR_PRECISION',
        'CALCULATOR_MAX_INPUT_VALUE',
        'CALCULATOR_DEFAULT_ENCODING'
    )

    config = CalculatorConfig()

    assert config.max_history_size == 1000
    assert config.precision == 10
    assert config.max_input_value == Decimal("1e999")
    assert config.default_encoding == 'utf-8'


def test_log_dir_property():
    """Ensure log_dir property defaults correctly."""
    clear_env_vars('CALCULATOR_LOG_DIR')

    config = CalculatorConfig(base_dir=Path('/new_base_dir'))

    assert config.log_dir == Path('/new_base_dir/logs').resolve()


def test_log_file_property():
    """Ensure log_file property defaults correctly."""
    clear_env_vars('CALCULATOR_LOG_FILE')

    config = CalculatorConfig(base_dir=Path('/new_base_dir'))

    assert config.log_file == Path('/new_base_dir/logs/calculator.log').resolve()


def test_history_dir_property():
    """Ensure history_dir property defaults correctly."""
    clear_env_vars('CALCULATOR_HISTORY_DIR')

    config = CalculatorConfig(base_dir=Path('/new_base_dir'))

    assert config.history_dir == Path('/new_base_dir/history').resolve()


def test_history_file_property():
    """Ensure history_file property defaults correctly."""
    clear_env_vars('CALCULATOR_HISTORY_FILE')

    config = CalculatorConfig(base_dir=Path('/new_base_dir'))

    assert config.history_file == Path('/new_base_dir/history/calculator_history.csv').resolve()

# Python Modules
import pytest

# App Imports
from app.validators import InputValidator
from app.exceptions import ValidationError


def test_validate_number_string_int():
    """String integer input should be converted to int."""
    assert InputValidator.validate_number("42") == 42


def test_validate_number_string_float():
    """String float input should be converted to float."""
    assert InputValidator.validate_number("3.14") == 3.14


def test_validate_number_string_with_whitespace():
    """Strings with leading/trailing whitespace are stripped and converted."""
    assert InputValidator.validate_number("  7  ") == 7


def test_validate_number_int_passthrough():
    """Integer input should be returned unchanged."""
    assert InputValidator.validate_number(10) == 10


def test_validate_number_float_passthrough():
    """Float input should be returned unchanged."""
    assert InputValidator.validate_number(2.5) == 2.5


def test_validate_number_invalid_type():
    """Non-numeric types should raise ValidationError."""
    with pytest.raises(ValidationError, match="Invalid value type"):
        InputValidator.validate_number([1, 2, 3])

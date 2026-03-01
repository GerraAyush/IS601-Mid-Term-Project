# Python Modules
import pytest

# App Imports
from app.validators import InputValidator
from app.exceptions import ValidationError


def test_validate_number_string_int():
    assert InputValidator.validate_number("42") == 42

def test_validate_number_string_float():
    assert InputValidator.validate_number("3.14") == 3.14

def test_validate_number_string_with_whitespace():
    assert InputValidator.validate_number("  7  ") == 7

def test_validate_number_int_passthrough():
    assert InputValidator.validate_number(10) == 10

def test_validate_number_float_passthrough():
    assert InputValidator.validate_number(2.5) == 2.5

def test_validate_number_invalid_type():
    with pytest.raises(ValidationError, match="Invalid value type"):
        InputValidator.validate_number([1, 2, 3])
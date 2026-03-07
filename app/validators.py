# Datatypes
from typing import Any

# App Imports
from app.datatypes import Number
from app.exceptions import ValidationError


class InputValidator:
    """
    Utility class for validating user inputs or values before performing
    calculator operations.
    """

    @staticmethod
    def validate_number(value: Any) -> Number:
        """
        Validate that the given value is a numeric type (int or float).
        Converts strings containing numeric values to int or float.

        Args:
            value (Any): The input value to validate.

        Returns:
            Number: The validated numeric value (int or float).

        Raises:
            ValidationError: If the value is not a valid number.
        """
        # If input is a string, try to convert to int or float
        if isinstance(value, str):
            value = value.strip()  # remove leading/trailing whitespace
            value = float(value) if '.' in value else int(value)
        
        # Ensure the value is now a numeric type
        if not isinstance(value, Number):
            raise ValidationError(f"Invalid value type: {type(value)}")
        
        return value

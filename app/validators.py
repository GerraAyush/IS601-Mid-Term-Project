# Datatypes
from typing import Any

# App Imports
from app.datatypes import Number
from app.exceptions import ValidationError

class InputValidator:
    
    @staticmethod
    def validate_number(value: Any) -> Number:
        if isinstance(value, str):
            value = value.strip()
            value = float(value) if '.' in value else int(value)
        
        if not isinstance(value, Number):
            raise ValidationError(f"Invalid value type: {type(value)}")
        
        return value
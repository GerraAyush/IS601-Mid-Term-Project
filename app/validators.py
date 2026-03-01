# Datatypes
from typing import Any

# App Imports
from app.datatypes import Number

class InputValidator:
    
    @staticmethod
    def validate_number(value: Any) -> Number:
        if isinstance(value, str):
            value = value.strip()
            value = float(value) if '.' in value else int(value)
        
        if not isinstance(value, Number):
            raise TypeError(f"Invalid value type: {type(value)}")
        
        return value
class CalculatorError(Exception):
    """
    Base exception class for all calculator-related errors.
    
    This allows catching any calculator-specific exception using CalculatorError.
    """
    pass

class OperationError(CalculatorError):
    """
    Raised when an error occurs during the execution of a calculation or operation.
    
    Examples:
        - Unsupported operation
    """
    pass

class ValidationError(CalculatorError):
    """
    Raised when input validation fails.
    
    Examples:
        - Operand is not a number
        - Operand exceeds allowed limits
    """
    pass

class ConfigurationError(CalculatorError):
    """
    Raised when there is a problem with calculator configuration.
    
    Examples:
        - Invalid max history size
        - Logging directory does not exist
        - Invalid precision value
    """
    pass

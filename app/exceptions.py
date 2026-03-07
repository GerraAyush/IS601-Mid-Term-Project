class CalculatorError(Exception):
    """
    Base exception for all calculator-related errors.

    All custom exceptions in the calculator application inherit from
    this class, allowing callers to catch any calculator-specific
    error using a single exception type.
    """
    pass


class OperationError(CalculatorError):
    """
    Raised when an error occurs during a calculation or operation.

    Examples
    --------
    - Unsupported operation
    - Division by zero
    - Invalid operation arguments
    """
    pass


class ValidationError(CalculatorError):
    """
    Raised when user input fails validation checks.

    Examples
    --------
    - Operand is not a valid number
    - Operand exceeds allowed limits
    - Incorrect number of arguments
    """
    pass


class ConfigurationError(CalculatorError):
    """
    Raised when application configuration is invalid.

    Examples
    --------
    - Invalid max history size
    - Invalid precision value
    - Missing or invalid configuration values
    """
    pass


class ExitSignal(Exception):
    """
    Internal control-flow exception used to terminate the REPL.

    This exception is raised by the ExitCommand to signal that the
    application should exit. It is not treated as an error but as a
    normal shutdown mechanism.
    """
    pass

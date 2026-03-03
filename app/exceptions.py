class CalculatorError(Exception):
    pass

class OperationError(CalculatorError):
    pass

class ValidationError(CalculatorError):
    pass

class ConfigurationError(CalculatorError):
    pass
# Datatypes
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

# App Imports
from app.datatypes import Number
from app.exceptions import ValidationError


@dataclass(frozen=True)
class Operation(metaclass=ABCMeta):
    cmd: str

    @abstractmethod
    def execute(self, a: Number, b: Number) -> Number:
        pass # pragma: no cover

    def validate_operands(self, a: Number, b: Number) -> None:
        if not isinstance(a, Number) or not isinstance(b, Number):
            raise ValidationError()
    
    def __str__(self) -> str:
        return self.__class__.__name__

class Addition(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a + b

class Subtraction(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a - b

class Multiplication(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a * b

class Division(Operation):
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a / b

class Power(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** b

class Root(Operation):
    def validate_operands(self, a: Number, b: Number) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Index cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a ** (1 / b)

class Modulus(Operation):
    def validate_operands(self, a, b) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a % b
    
class IntegerDivision(Operation):
    def validate_operands(self, a, b) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return a // b
    
class Percentage(Operation):
    def validate_operands(self, a, b) -> None:
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Base cannot be zero.")
    
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return (a / b) * 100
    
class AbsoluteDifference(Operation):
    def execute(self, a: Number, b: Number) -> Number:
        self.validate_operands(a, b)
        return abs(a - b)

class OperationFactory:
    _operation_dict = {
        'add' : {
            '_cls' : Addition,
            'desc' : 'perform addition of two numbers',
        },
        'subtract' : {
            '_cls' : Subtraction,
            'desc' : 'perform subtraction of two numbers',
        },
        'multiply' : {
            '_cls' : Multiplication,
            'desc' : 'perform multiplication of two numbers',
        },
        'divide' : {
            '_cls' : Division,
            'desc' : 'perform division of a by b',
        },
        'power' : {
            '_cls' : Power,
            'desc' : 'perform a to the power of b',
        },
        'root' : {
            '_cls' : Root,
            'desc' : 'perform bth root of a',
        },
        'modulus' : {
            '_cls' : Modulus,
            'desc' : 'check divisibility of a wrt b',
        },
        'idivide' : {
            '_cls' : IntegerDivision,
            'desc' : 'perform integer division of a by b',
        },
        'percentage' : {
            '_cls' : Percentage,
            'desc' : 'check how much percent of b is a',
        },
        'abs-diff' : {
            '_cls' : AbsoluteDifference,
            'desc' : 'perform absolute difference of a and b',
        }
    }

    @classmethod
    def is_registered(cls, operation_name: str) -> bool:
        return operation_name.lower() in cls._operation_dict

    @classmethod
    def register_operation(
        cls,
        operation_name: str, 
        operation_class: Operation, 
        operation_description: str
    ) -> None:
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operation_dict.update(
            {
                operation_name.lower() : { 
                    "_cls" : operation_class, 
                    "desc" : operation_description
                } 
            }
        )

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        operation_info = cls._operation_dict.get(operation_name.lower())
        if not operation_info:
            raise ValueError(f"Unregistered Operation: {operation_name}")
        return operation_info.get("_cls")(cmd=operation_name)
    
    @classmethod
    def list_operations(cls):
        display_string = ""
        for cmd, operation_info in cls._operation_dict.items():
            display_string += f"  {cmd} - {operation_info['desc']}\n"
        return display_string.rstrip()

# Datatypes
from typing import Type

# App Imports
from app.factory import FactoryBase


def register(factory: Type[FactoryBase], name: str, description: str):
    """
    Generic decorator used to register classes into a factory.

    This allows commands and operations to automatically register
    themselves in their respective factories when the class is defined.

    Args:
        factory (Type[FactoryBase]): Factory where the class should be registered.
        name (str): Command/operation name used in the REPL.
        description (str): Description shown in help.
    """

    def decorator(cls):
        factory.register(name=name, item_class=cls, description=description)
        return cls

    return decorator


def operation(name: str, description: str):
    """
    Decorator used to register an Operation class.
    Import done lazily to avoid circular imports.
    """
    from app.operation import OperationFactory

    return register(OperationFactory, name=name, description=description)


def command(name: str, description: str):
    """
    Decorator used to register a Command class.
    Import done lazily to avoid circular imports.
    """
    from app.command import ReplCommandFactory

    return register(ReplCommandFactory, name=name, description=description)

# Python Modules
import pytest

# App Imports
from app.registry import register, operation, command
from app.factory import FactoryBase
from app.operation import OperationFactory, Operation
from app.command import ReplCommandFactory, Command


def test_register_decorator_registers_class():
    """Test that the generic register decorator registers a class in the given factory."""

    class DummyBase:
        pass

    class DummyFactory(FactoryBase):
        _item_dict = {}
        _base_class = DummyBase

    @register(DummyFactory, name="dummy", description="dummy item")
    class DummyItem(DummyBase):
        pass

    assert "dummy" in DummyFactory._item_dict
    assert DummyFactory._item_dict["dummy"]["_cls"] is DummyItem
    assert DummyFactory._item_dict["dummy"]["desc"] == "dummy item"


def test_operation_decorator_registers_operation():
    """Test that the operation decorator registers an Operation subclass."""

    @operation("test_add", "test addition")
    class TestOperation(Operation):
        def execute(self, a, b):
            return a + b

    assert OperationFactory.is_registered("test_add")

    instance = OperationFactory.create("test_add")
    assert isinstance(instance, TestOperation)


def test_command_decorator_registers_command():
    """Test that the command decorator registers a Command subclass."""

    @command("test_cmd", "test command")
    class TestCommand(Command):
        def execute(self):
            return None

    assert ReplCommandFactory.is_registered("test_cmd")

    instance = ReplCommandFactory.create("test_cmd")
    assert isinstance(instance, TestCommand)


def test_register_returns_original_class():
    """Ensure the decorator returns the original class unchanged."""

    class DummyBase:
        pass

    class DummyFactory(FactoryBase):
        _item_dict = {}
        _base_class = DummyBase

    @register(DummyFactory, name="check", description="check item")
    class DummyItem(DummyBase):
        pass

    assert DummyItem.__name__ == "DummyItem"

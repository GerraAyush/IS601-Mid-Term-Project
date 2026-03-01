# Python Modules
import pytest
from datetime import datetime
from unittest.mock import patch

# App Imports
from app.calculation import Calculation


class FakeOperation:
    def __init__(self, name="add"):
        self.name = name

    def execute(self, a, b):
        return a + b

    def __str__(self):
        return self.name
    

@pytest.fixture
def fake_operation():
    return FakeOperation("Addition")

@pytest.fixture
def mock_factory(fake_operation):
    with patch("app.calculation.OperationFactory.create_operation") as mock:
        mock.return_value = fake_operation
        yield mock

def test_post_init_sets_operation_and_result(mock_factory):
    calc = Calculation("add", 2, 3)
    assert calc._operation_cls == "Addition"
    assert calc._result == 5
    mock_factory.assert_called_once_with("add")

def test_str_representation(mock_factory):
    calc = Calculation("add", 4, 6)
    assert str(calc) == "Addition(4, 6) = 10"

def test_repr_representation(mock_factory):
    calc = Calculation("add", 1, 2)
    expected_start = "Calculation(operation='add', operand1=1, operand2=2, result=3, timestamp='"
    assert repr(calc).startswith(expected_start)
    assert calc._timestamp.isoformat() in repr(calc)

def test_timestamp_auto_generated(mock_factory):
    before = datetime.now()
    calc = Calculation("add", 5, 5)
    after = datetime.now()
    assert before <= calc._timestamp <= after

def test_equality_true(mock_factory):
    calc1 = Calculation("add", 2, 3)
    calc2 = Calculation("add", 2, 3)
    assert calc1 == calc2

def test_equality_false_different_values(mock_factory):
    calc1 = Calculation("add", 2, 3)
    calc2 = Calculation("add", 3, 4)
    assert calc1 != calc2

def test_equality_not_implemented(mock_factory):
    calc = Calculation("add", 1, 2)
    assert calc.__eq__(123) is NotImplemented

def test_frozen_dataclass(mock_factory):
    calc = Calculation("add", 1, 2)
    with pytest.raises(Exception):
        calc._operand1 = 10
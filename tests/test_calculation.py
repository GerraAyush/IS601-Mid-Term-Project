# Python Modules
import pytest
from datetime import datetime
from unittest.mock import patch

# App Imports
from app.calculation import Calculation
from app.exceptions import OperationError
from app.datatypes import Number


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
    calculation = Calculation("add", 2, 3)
    assert calculation._operation_class == "Addition"
    assert calculation._result == 5
    mock_factory.assert_called_once_with("add")

def test_str_representation(mock_factory):
    calculation = Calculation("add", 4, 6)
    assert str(calculation) == "Addition(4, 6) = 10"

def test_repr_representation(mock_factory):
    calculation = Calculation("add", 1, 2)
    expected_start = "Calculation(operation_name='add', operand1=1, operand2=2, operation_class='Addition', result=3, timestamp='"
    assert repr(calculation).startswith(expected_start)
    assert calculation._timestamp.isoformat() in repr(calculation)

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

def test_to_dict():
    calculation = Calculation(_operation_name="add", _operand1=2, _operand2=3)
    result_dict = calculation.to_dict()
    assert result_dict == {
        "operation_name": "add",
        "operand1": 2,
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": calculation._timestamp.isoformat()
    }

def test_from_dict():
    data = {
        "operation_name": "add",
        "operand1": 2,
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": datetime.now().isoformat()
    }
    calculation = Calculation.from_dict(data)
    assert calculation._operation_name == "add"
    assert calculation._operand1 == 2
    assert calculation._operand2 == 3
    assert calculation._result == 5
    assert calculation._operation_class == "Addition"
    assert calculation._timestamp == data["timestamp"]

def test_invalid_from_dict():
    data = {
        "operation_name": "add",
        "operand1": "invalid",
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Operation failed"):
        Calculation.from_dict(data)

# Python Modules
import pytest
import logging
from datetime import datetime

# App Imports
from app.calculation import Calculation
from app.exceptions import OperationError

def test_post_init_sets_operation_and_result(mock_factory):
    """Ensure __post_init__ sets operation class and computes result."""
    calculation = Calculation("add", 2, 3)

    # Operation class name should match the factory return
    assert calculation._operation_class == "Addition"

    # Result should be computed correctly
    assert calculation._result == 5

    # Ensure factory was called correctly
    mock_factory.assert_called_once_with("add")


def test_str_representation(mock_factory):
    """Verify user-friendly string representation."""
    calculation = Calculation("add", 4, 6)

    # __str__ should produce readable calculation output
    assert str(calculation) == "Addition(4, 6) = 10"


def test_repr_representation(mock_factory):
    """Verify developer-friendly representation string."""
    calculation = Calculation("add", 1, 2)

    expected_start = (
        "Calculation(operation_name='add', operand1=1, operand2=2, "
        "operation_class='Addition', result=3, timestamp='"
    )

    # repr should start with expected structured output
    assert repr(calculation).startswith(expected_start)

    # Timestamp should appear in the representation
    assert calculation._timestamp.isoformat() in repr(calculation)


def test_timestamp_auto_generated(mock_factory):
    """Ensure timestamp is automatically generated during initialization."""
    before = datetime.now()
    calc = Calculation("add", 5, 5)
    after = datetime.now()

    # Timestamp should fall between creation boundaries
    assert before <= calc._timestamp <= after


def test_equality_true(mock_factory):
    """Verify equality comparison for identical calculations."""
    calc1 = Calculation("add", 2, 3)
    calc2 = Calculation("add", 2, 3)

    # Objects with identical values should be equal
    assert calc1 == calc2


def test_equality_false_different_values(mock_factory):
    """Verify equality returns False for different calculations."""
    calc1 = Calculation("add", 2, 3)
    calc2 = Calculation("add", 3, 4)

    assert calc1 != calc2


def test_equality_not_implemented(mock_factory):
    """Ensure equality returns NotImplemented for unrelated types."""
    calc = Calculation("add", 1, 2)

    # Comparison with non-Calculation object
    assert calc.__eq__(123) is NotImplemented


def test_frozen_dataclass(mock_factory):
    """Ensure dataclass immutability prevents attribute modification."""
    calc = Calculation("add", 1, 2)

    # Frozen dataclass should raise exception when mutated
    with pytest.raises(Exception):
        calc._operand1 = 10


def test_to_dict():
    """Verify conversion of Calculation object to dictionary."""
    calculation = Calculation(_operation_name="add", _operand1=2, _operand2=3)

    result_dict = calculation.to_dict()

    # Ensure dictionary structure and values are correct
    assert result_dict == {
        "operation_name": "add",
        "operand1": 2,
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": calculation._timestamp.isoformat()
    }


def test_from_dict():
    """Verify Calculation object can be reconstructed from dictionary."""
    data = {
        "operation_name": "add",
        "operand1": 2,
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": datetime.now().isoformat()
    }

    calculation = Calculation.from_dict(data)

    # Ensure attributes match dictionary values
    assert calculation._operation_name == "add"
    assert calculation._operand1 == 2
    assert calculation._operand2 == 3
    assert calculation._result == 5
    assert calculation._operation_class == "Addition"
    assert calculation._timestamp == datetime.fromisoformat(data["timestamp"])


def test_invalid_from_dict():
    """Ensure invalid dictionary data raises OperationError."""
    data = {
        "operation_name": "add",
        "operand1": "invalid",  # Invalid operand
        "operand2": 3,
        "result": 5,
        "operation_class": "Addition",
        "timestamp": datetime.now().isoformat()
    }

    # Invalid operand should trigger operation failure
    with pytest.raises(OperationError, match="Operation failed"):
        Calculation.from_dict(data)


def test_result_mismatch_from_dict(caplog):
    """Verify warning is logged if stored result differs from computed result."""
    with caplog.at_level(logging.WARNING):
        data = {
            "operation_name": "add",
            "operand1": 2,
            "operand2": 3,
            "result": 10,  # Incorrect stored result
            "operation_class": "Addition",
            "timestamp": datetime.now().isoformat()
        }

        Calculation.from_dict(data)

        # Ensure warning message is logged
        assert "Loaded calculation result 10 differs from computed result 5" in caplog.text

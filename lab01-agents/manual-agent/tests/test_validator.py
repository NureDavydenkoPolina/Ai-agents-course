import pytest

from agent.errors import DecisionError
from agent.validator import validate_decision


def test_rejects_unknown_action():
    with pytest.raises(DecisionError):
        validate_decision({"action": "delete_all_files", "arguments": {}})


def test_rejects_missing_argument():
    with pytest.raises(DecisionError):
        validate_decision({"action": "lookup_renpy_statement", "arguments": {}})


def test_accepts_valid_decision():
    validate_decision({"action": "lookup_renpy_statement", "arguments": {"name": "jump"}})

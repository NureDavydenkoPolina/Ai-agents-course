import pytest

from agent.environment import NOT_FOUND, list_by_category
from agent.errors import DecisionError
from agent.loop import run_agent
from agent.validator import validate_decision


def test_list_by_category_found():
    assert list_by_category("control_flow") == "label, jump, call, return"


def test_list_by_category_missing():
    assert list_by_category("audio") == NOT_FOUND


def test_validator_requires_category():
    with pytest.raises(DecisionError):
        validate_decision({"action": "list_by_category", "arguments": {}})


def test_loop_uses_both_actions():
    decisions = iter([
        {"action": "list_by_category", "arguments": {"category": "control_flow"},
         "decision_summary": "x"},
        {"action": "lookup_renpy_statement", "arguments": {"name": "jump"},
         "decision_summary": "x"},
        {"action": "finish", "arguments": {"answer": "ok"}, "decision_summary": "x"},
    ])
    state = run_agent("Мета", decide=lambda *args: next(decisions))
    assert state.observations[0].startswith("category control_flow:")
    assert state.observations[1].startswith("jump:")
    assert state.stop_reason == "finish"

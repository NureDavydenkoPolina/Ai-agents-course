from agent.loop import run_agent


def scripted(decisions):
    """Підміна get_decision: повертає рішення зі списку по одному."""
    it = iter(decisions)

    def decide(goal, observations, step, max_steps):
        return next(it)

    return decide


LOOKUP_JUMP = {"action": "lookup_renpy_statement", "arguments": {"name": "jump"},
               "decision_summary": "need jump"}
FINISH = {"action": "finish", "arguments": {"answer": "готово"},
          "decision_summary": "enough data"}


def test_finishes_on_finish_action():
    state = run_agent("Розкажи про jump", decide=scripted([LOOKUP_JUMP, FINISH]))
    assert state.stop_reason == "finish"
    assert state.final_answer == "готово"
    assert state.llm_calls == 2
    assert state.observations[0].startswith("jump:")


def test_stops_on_max_steps():
    forever = lambda *args: LOOKUP_JUMP  # модель ніколи не завершує
    state = run_agent("Нескінченна мета", decide=forever, max_steps=3)
    assert state.stop_reason == "max_steps"
    assert state.step == 3
    assert state.llm_calls == 3


def test_unknown_action_becomes_observation():
    bad = {"action": "delete_all_files", "arguments": {}, "decision_summary": "x"}
    state = run_agent("Мета", decide=scripted([bad, FINISH]))
    assert state.observations[0].startswith("ERROR:")
    assert state.trace[0]["action"] == "rejected"
    assert state.stop_reason == "finish"


def test_missing_statement_gives_not_found():
    missing = {"action": "lookup_renpy_statement", "arguments": {"name": "python"},
               "decision_summary": "x"}
    state = run_agent("Опиши python", decide=scripted([missing, FINISH]))
    assert state.observations[0] == "python: NOT_FOUND"

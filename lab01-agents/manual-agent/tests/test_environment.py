from agent.environment import NOT_FOUND, STATEMENTS, lookup_renpy_statement


def test_lookup_existing_statement():
    result = lookup_renpy_statement("jump")
    assert result == STATEMENTS["jump"]
    assert "без збереження місця повернення" in result


def test_lookup_missing_statement():
    assert lookup_renpy_statement("python") == NOT_FOUND


def test_lookup_normalizes_argument():
    assert lookup_renpy_statement("  MENU ") == STATEMENTS["menu"]


def test_environment_size_and_ids():
    assert 5 <= len(STATEMENTS) <= 10
    for key in STATEMENTS:
        assert key == key.lower() and key.isascii()

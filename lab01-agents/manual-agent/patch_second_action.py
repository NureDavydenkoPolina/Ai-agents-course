from pathlib import Path


def patch(path, old, new):
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"{path}: фрагмент знайдено {text.count(old)} раз: {old[:40]!r}"
    p.write_text(text.replace(old, new), encoding="utf-8")
    print("ok:", path)


# 1. середовище: нова функція в кінець файла
env = Path("agent/environment.py")
env.write_text(env.read_text(encoding="utf-8") + '''

# Категорії за розділами документації Ren'Py
CATEGORIES: dict[str, tuple[str, ...]] = {
    "control_flow": ("label", "jump", "call", "return"),  # Labels & Control Flow
    "choices": ("menu",),  # In-Game Menus
    "images": ("scene", "show", "hide", "with"),  # Displaying Images
}


def list_by_category(category: str) -> str:
    """Return the Ren'Py statements that belong to one documentation category.

    Use it when the user asks which statements exist in a group, for example
    statements that control the story flow.

    Args:
        category: One of "control_flow", "choices", "images".

    Returns:
        Comma-separated statement names, or the string "NOT_FOUND" if the
        category does not exist.
    """
    key = category.strip().lower().replace("-", "_").replace(" ", "_")
    names = CATEGORIES.get(key)
    return ", ".join(names) if names else NOT_FOUND
''', encoding="utf-8")
print("ok: agent/environment.py")

# 2. валідатор
patch("agent/validator.py",
      '    "finish": {"answer"},',
      '    "list_by_category": {"category"},\n    "finish": {"answer"},')

# 3. диспетчер
patch("agent/loop.py",
      "from .environment import lookup_renpy_statement",
      "from .environment import list_by_category, lookup_renpy_statement")
patch("agent/loop.py",
      '    if action == "finish":\n',
      '    if action == "list_by_category":\n'
      '        category = args["category"]\n'
      '        return f"category {category}: {list_by_category(category)}"\n'
      '    if action == "finish":\n')

# 4. інструкція компонента прийняття рішень
patch("agent/reasoning.py",
      "2. finish\n",
      "2. list_by_category\n"
      "   Use it when you need to know which statements belong to a group.\n"
      '   Arguments: {"category": string} one of "control_flow", "choices", "images"\n'
      "3. finish\n")
patch("agent/reasoning.py",
      '"action": "lookup_renpy_statement | finish"',
      '"action": "lookup_renpy_statement | list_by_category | finish"')
patch("agent/reasoning.py",
      "AVAILABLE ACTIONS: lookup_renpy_statement, finish",
      "AVAILABLE ACTIONS: lookup_renpy_statement, list_by_category, finish")

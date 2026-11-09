"""Середовище агента: перевірені відомості про оператори сценарію Ren'Py.

Детермінований код без LLM. Джерела фактів: офіційна документація Ren'Py:
- Labels & Control Flow: https://www.renpy.org/doc/html/label.html
- In-Game Menus: https://www.renpy.org/doc/html/menus.html
- Displaying Images: https://www.renpy.org/doc/html/displaying_images.html
"""

STATEMENTS: dict[str, str] = {
    "label": (
        "label дає назву точці в сценарії, на яку можна перейти через "
        "jump або call. Синтаксис: label назва:."
    ),
    "jump": (
        "jump передає керування на вказану мітку без збереження місця "
        "повернення. На відміну від call, він не кладе наступний оператор "
        "у стек викликів."
    ),
    "call": (
        "call передає керування на вказану мітку і кладе наступний оператор "
        "у стек викликів, щоб після return виконання продовжилося з нього."
    ),
    "return": (
        "return забирає верхній запис зі стека викликів і повертає керування "
        "туди. Якщо стек порожній, Ren'Py перезапускається й повертає гравця "
        "в головне меню."
    ),
    "menu": (
        "menu показує гравцеві вибір із кількох варіантів; обраний варіант "
        "виконує свій блок, після чого виконання йде далі після menu. "
        "Варіант може мати умову if і показується лише тоді, коли вона істинна."
    ),
    "scene": (
        "scene прибирає всі зображення з шару й показує на ньому нове "
        "зображення. Без назви зображення лише очищає шар."
    ),
    "show": (
        "show показує зображення на шарі. Нове зображення з тим самим тегом "
        "замінює попереднє."
    ),
    "hide": "hide прибирає зображення з шару.",
    "with": (
        "with застосовує ефект переходу під час зміни сцени. "
        "with None означає відсутність видимого переходу."
    ),
}

NOT_FOUND = "NOT_FOUND"


def normalize_name(name: str) -> str:
    """Зводить ' Jump ', 'JUMP' до ключа 'jump'."""
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def lookup_renpy_statement(name: str) -> str:
    """Return verified information about one Ren'Py script statement.

    Use it when the user asks about a specific Ren'Py statement such as
    label, jump, call, return, menu, scene, show, hide or with.

    Args:
        name: Statement name, e.g. "jump" or "Menu". Case is ignored.

    Returns:
        A short verified description, or the string "NOT_FOUND" if the
        statement is not in the environment.
    """
    return STATEMENTS.get(normalize_name(name), NOT_FOUND)

import os

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .environment import list_by_category, lookup_renpy_statement

MODEL = "gemini-3.5-flash"

INSTRUCTION = """
ROLE: навчальний агент з операторів сценарію Ren'Py для авторів візуальних новел.

PURPOSE: відповідати на питання про конкретні оператори Ren'Py лише на основі
перевірених даних, які повертають інструменти lookup_renpy_statement і list_by_category.

LANGUAGE: українська, якщо користувач не попросив іншу мову.

BEHAVIOR RULES:
1. Перед відповіддю про конкретний оператор виклич lookup_renpy_statement
   для кожного згаданого оператора окремо.
2. Якщо результат дорівнює NOT_FOUND, прямо скажи, що перевірених даних
   про цей оператор немає, і не добудовуй відповідь із власних знань.
3. У відповіді про конкретні оператори використовуй лише факти з результатів
   інструмента.
4. На загальні питання (що таке Ren'Py, що таке візуальна новела) відповідай
   коротко без інструмента.
5. Не викликай інструмент повторно з тим самим аргументом.
6. Якщо питають, які оператори належать до групи (control_flow, choices,
   images), виклич list_by_category, а для деталей про окремі оператори
   виклич lookup_renpy_statement.

LIMITATIONS: не виконуй дій, для яких немає інструментів; не вигадуй джерел;
не пиши і не виправляй код користувача.
"""


def _build_model():
    """Gemini API за замовчуванням; локальна модель Ollama при USE_OLLAMA=1."""
    if os.getenv("USE_OLLAMA") == "1":
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model="ollama_chat/qwen2.5:7b")
    return Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    )


root_agent = Agent(
    name="root_agent",
    model=_build_model(),
    instruction=INSTRUCTION,
    tools=[lookup_renpy_statement, list_by_category],
)

app = App(
    root_agent=root_agent,
    name="app",  # має збігатися з назвою каталогу агента
)

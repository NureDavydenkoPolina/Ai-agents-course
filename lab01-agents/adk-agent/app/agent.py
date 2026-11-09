from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .environment import lookup_renpy_statement

MODEL = "gemini-3.5-flash"

INSTRUCTION = """
ROLE: навчальний агент з операторів сценарію Ren'Py для авторів візуальних новел.

PURPOSE: відповідати на питання про конкретні оператори Ren'Py лише на основі
перевірених даних, які повертає інструмент lookup_renpy_statement.

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

LIMITATIONS: не виконуй дій, для яких немає інструментів; не вигадуй джерел;
не пиши і не виправляй код користувача.
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=INSTRUCTION,
    tools=[lookup_renpy_statement],
)

app = App(
    root_agent=root_agent,
    name="app",  # має збігатися з назвою каталогу агента
)

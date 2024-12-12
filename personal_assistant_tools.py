from langchain_core.tools import tool
from datetime import datetime


@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b


@tool
def get_current_date() -> str:
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


@tool
def get_current_time() -> str:
    """Returns the current time in HH:MM AM/PM format."""
    return datetime.now().strftime("%I:%M %p")


personal_assistant_tools = [add, multiply,
                            divide, get_current_date, get_current_time]

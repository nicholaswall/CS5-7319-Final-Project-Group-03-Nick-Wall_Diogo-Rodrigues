import sqlite3
from typing import List as ListType

con = sqlite3.connect("tasks.db")


def sql_stringify(x: str) -> str:
    return "'" + str(x) + "'"


def sql_stringify_list(items: ListType[str]) -> str:
    """
    For each item in the list, add a single quote to the beginning and end of the item.
    Then, join all the items together with a comma.
    """
    return ", ".join([sql_stringify(item) for item in items])


def sql_value(items: ListType[str]) -> str:
    """
    Stringigy the list and surround with parenthesis.
    """
    return "(" + sql_stringify_list(items) + ")"

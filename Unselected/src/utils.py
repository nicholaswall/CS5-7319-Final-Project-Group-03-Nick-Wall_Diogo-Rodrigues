from dataclasses import dataclass
from Selected.src.db import con

CURSOR = con.cursor()
LIST_TABLE_NAME = "lists"
TASK_TABLE_NAME = "tasks"


def set_up_db():
    # Create Lists table
    sql = (
        "CREATE TABLE IF NOT EXISTS "
        + LIST_TABLE_NAME
        + " (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL)"
    )
    CURSOR.execute(sql)

    # Create Tasks table
    sql = (
        "CREATE TABLE IF NOT EXISTS "
        + TASK_TABLE_NAME
        + """ (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT FALSE,
            list_id INTEGER NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY(list_id) REFERENCES lists(id),
            FOREIGN KEY(parent_id) REFERENCES tasks(id)
            )
        """
    )
    CURSOR.execute(sql)


@dataclass
class TaskList:
    def __init__(self, name, id=-1, description=None):
        self.name = name
        self.id = id
        self.description = description

    def __eq__(self, obj):
        return isinstance(obj, TaskList) and self.id == obj.id

    def __str__(self) -> str:
        if self.description:
            return f'{self.name}: "{self.description}"'
        else:
            return self.name


@dataclass
class Task:
    def __init__(
        self,
        title,
        id=-1,
        description=None,
        completed=False,
        list_id=-1,
        parent_id=None,
        list_name=None,
        parent_name=None,
    ):
        self.title = title
        self.id = id
        self.description = description
        self.completed = completed
        self.list_id = list_id
        self.list_name = list_name
        self.parent_id = parent_id
        self.parent_name = parent_name

    def __eq__(self, obj):
        return isinstance(obj, Task) and self.id == obj.id and self.title == obj.title

    def __lt__(self, obj):
        return self.title.lower() < obj.title.lower()

    def __gt__(self, obj):
        return self.title.lower() > obj.title.lower()

    def __str__(self) -> str:
        return f'{self.title}: "{self.description}". ID: {self.id}. Completed: {self.completed}. List: {self.list_name}. Parent: {self.parent_name}'

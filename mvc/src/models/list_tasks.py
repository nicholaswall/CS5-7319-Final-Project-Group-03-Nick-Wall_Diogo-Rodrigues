from typing import List as ListType
from dataclasses import dataclass
from mvc.src.models.lists import List
from mvc.src.models.tasks import Task


@dataclass
class ListTasks:
    list: List
    tasks: ListType[Task]

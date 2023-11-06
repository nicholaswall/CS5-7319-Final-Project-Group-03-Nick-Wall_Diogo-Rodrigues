from typing import List as ListType
from dataclasses import dataclass
from Selected.src.models.lists import List
from Selected.src.models.tasks import Task


@dataclass
class ListTasks:
    list: List
    tasks: ListType[Task]

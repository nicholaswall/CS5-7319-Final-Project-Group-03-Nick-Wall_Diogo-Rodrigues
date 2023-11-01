from typing import Optional
from mvc.src.views.base import View
from mvc.src.models.tasks import Task


class CreatedTaskView(View):
    def __init__(
        self,
        created_task: Task,
        list_name: str,
        parent_task_title: Optional[str] = None,
    ):
        self.created_task = created_task
        self.list_name = list_name
        self.parent_task_title = parent_task_title

    def render(self):
        print("Created task: ")
        print("\t", "Name:", self.created_task.title)
        print("\t", "Description", self.created_task.description)
        print("\t", "List:", self.list_name)
        if self.parent_task_title:
            print("\t", "Parent Task:", self.parent_task_title)
        print("\t", "Completed:", "Yes" if self.created_task.completed else "No")

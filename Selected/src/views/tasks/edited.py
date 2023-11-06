from Selected.src.views.base import View
from Selected.src.models.tasks import Task


class EditedTaskView(View):
    def __init__(
        self,
        original_task: Task,
        original_task_parent_title: str,
        edited_task: Task,
        edited_task_parent_title: str,
    ):
        self.original_task = original_task
        self.original_task_parent_title = original_task_parent_title
        self.edited_task = edited_task
        self.edited_task_parent_title = edited_task_parent_title

    def render(self):
        print("Edited task: ")
        print(f"\tName: {self.original_task.title} -> {self.edited_task.title}")
        print(
            f"\tDescription: {self.original_task.description} -> {self.edited_task.description}"
        )
        print(
            f"\tParent: {self.original_task_parent_title} -> {self.edited_task_parent_title}"
        )

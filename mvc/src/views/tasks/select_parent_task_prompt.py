from mvc.src.prompter import Prompter
from mvc.src.views.base import View
from typing import List as ListType, Optional
from mvc.src.models.tasks import Task


class SelectParentTaskPromptView(View):
    def __init__(self, tasks: ListType[Task]):
        self.tasks = tasks
        self.prompter = Prompter(
            "What is the parent task's title? (optional): ", False, str
        )

    def render(self) -> Optional[str]:
        print("Available parent tasks:")
        for task in self.tasks:
            print("\t", task.title)
        parent_task_name = self.prompter.ask()
        return parent_task_name

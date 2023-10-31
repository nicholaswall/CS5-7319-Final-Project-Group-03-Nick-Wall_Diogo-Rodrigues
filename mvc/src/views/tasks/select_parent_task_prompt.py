from mvc.src.views.base import View
from typing import List as ListType


class SelectParentTaskPromptView(View):
    def __init__(self, task_names: ListType[str]):
        self.task_names = task_names

    def render(self):
        parent_task_name = input("What is the parent task's title? (optional): ")
        return parent_task_name

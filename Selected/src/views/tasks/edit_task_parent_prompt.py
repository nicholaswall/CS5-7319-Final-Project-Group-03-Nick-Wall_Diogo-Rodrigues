from Selected.src.prompter import Prompter
from Selected.src.views.base import View
from Selected.src.models.tasks import Task
from typing import List as ListType


class EditTaskParentPromptView(View):
    def __init__(self, potential_parents: ListType[Task]):
        self.potential_parents = potential_parents
        self.new_parent_prompt = Prompter(
            "Parent task title",
            required=False,
            input_type=str,
            validation_func=lambda x: x
            in [task.title for task in self.potential_parents],
        )

    def render(self) -> str:
        print("Choose a new parent for your task:")
        for task in self.potential_parents:
            print(f"\t{task.title}: {task.description}")
        new_parent_name = self.new_parent_prompt.ask()

        return new_parent_name

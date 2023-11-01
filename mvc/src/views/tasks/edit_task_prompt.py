from mvc.src.prompter import Prompter
from mvc.src.views.base import View
from typing import Tuple, Optional


class EditTaskPromptView(View):
    def __init__(self):
        self.initial_name_prompter = Prompter(
            "Enter a name of a task to edit: ", required=True, input_type=str
        )
        self.name_prompter = Prompter(
            "Enter a new name for your task: ", required=False, input_type=str
        )
        self.description_prompter = Prompter(
            "Enter a description for your task: ", required=False, input_type=str
        )

    def render(self) -> Tuple[str, Optional[str], Optional[str]]:
        intial_task_name = self.initial_name_prompter.ask()
        print("Leave empty if you don't want to change the name or description")
        task_name = self.name_prompter.ask()
        task_description = self.description_prompter.ask()

        return intial_task_name, task_name, task_description

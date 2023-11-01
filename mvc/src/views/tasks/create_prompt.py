from mvc.src.prompter import Prompter
from mvc.src.views.base import View
from typing import Tuple, Optional


class CreateTaskPromptView(View):
    def __init__(self):
        self.name_prompter = Prompter(
            "Enter a name for your task: ", required=True, input_type=str
        )
        self.description_prompter = Prompter(
            "Enter a description for your task: ", required=False, input_type=str
        )

    def render(self) -> Tuple[str, Optional[str]]:
        task_name = self.name_prompter.ask()
        task_description = self.description_prompter.ask()

        return task_name, task_description

from mvc.src.prompter import Prompter
from mvc.src.views.base import View
from typing import Tuple, Optional


class DeleteTaskPromptView(View):
    def __init__(self):
        self.title_prompter = Prompter(
            "Enter a task title to delete: ", required=True, input_type=str
        )

    def render(self) -> Tuple[str, Optional[str]]:
        task_title = self.title_prompter.ask()
        return task_title

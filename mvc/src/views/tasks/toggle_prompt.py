from mvc.src.prompter import Prompter
from mvc.src.views.base import View


class ToggleTaskPromptView(View):
    def __init__(self):
        self.title_prompter = Prompter(
            "Enter a task title to change the completion status: ",
            required=True,
            input_type=str,
        )

    def render(self) -> str:
        task_title = self.title_prompter.ask()
        return task_title

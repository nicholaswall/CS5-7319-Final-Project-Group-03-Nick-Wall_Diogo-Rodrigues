from Selected.src.prompter import Prompter
from Selected.src.views.base import View


class DeleteTaskPromptView(View):
    def __init__(self):
        self.title_prompter = Prompter(
            "Enter a task title to delete", required=True, input_type=str
        )

    def render(self) -> str:
        task_title = self.title_prompter.ask()
        return task_title

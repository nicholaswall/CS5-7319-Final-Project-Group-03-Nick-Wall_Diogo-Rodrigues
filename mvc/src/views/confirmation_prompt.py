from mvc.src.prompter import Prompter
from mvc.src.views.base import View


class ConformationPromptView(View):
    def __init__(self):
        self.prompter = Prompter(
            "Are you sure: (y/n)",
            required=True,
            input_type=str,
            validation_func=lambda x: x in ["y", "n"],
        )

    def render(self):
        confirmation = self.prompter.ask()
        if confirmation == "y":
            return True
        return False

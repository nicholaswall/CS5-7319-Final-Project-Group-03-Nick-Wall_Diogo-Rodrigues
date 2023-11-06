from Selected.src.views.base import View
from Selected.src.prompter import Prompter
from typing import Tuple, Optional


class CreateListPromptView(View):
    def __init__(self):
        self.name_prompter = Prompter(
            "Enter a name for your list", required=True, input_type=str
        )
        self.description_prompter = Prompter(
            "Enter a description for your list", required=False, input_type=str
        )

    def render(self) -> Tuple[str, Optional[str]]:
        list_name = self.name_prompter.ask()
        list_description = self.description_prompter.ask()
        return list_name, list_description

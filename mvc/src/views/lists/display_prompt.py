from typing import Optional
from mvc.src.views.base import View
from mvc.src.prompter import Prompter


class DisplayListPromptView(View):
    def __init__(self):
        self.prompter = Prompter(
            "Enter a search to filter by (leave empty for no filter): ",
            required=False,
            input_type=str,
        )

    def render(self) -> Optional[str]:
        list_name = self.prompter.ask()
        return list_name

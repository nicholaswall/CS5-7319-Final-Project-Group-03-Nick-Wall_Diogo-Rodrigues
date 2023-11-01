from mvc.src.prompter import Prompter
from mvc.src.views.base import View
from typing import List as ListType
from mvc.src.models.lists import List


class SelectListPromptView(View):
    def __init__(self, lists: ListType[List]):
        self.lists = lists
        self.prompter = Prompter("What list should this task belong to?: ", True, str)

    def render(self) -> str:
        print("Available lists:")
        for list in self.lists:
            print("\t", list.name)

        list_name = self.prompter.ask()
        return list_name

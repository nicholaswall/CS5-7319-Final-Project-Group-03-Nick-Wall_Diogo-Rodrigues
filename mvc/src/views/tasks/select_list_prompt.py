from mvc.src.views.base import View
from typing import List as ListType
from mvc.src.models.lists import List


class SelectListPromptView(View):
    def __init__(self, lists: ListType[List]):
        self.lists = lists

    def render(self):
        print("Available lists:")
        for list in self.lists:
            print("\t", list.name)

        list_name = input("What list should this task belong to?: ")
        return list_name

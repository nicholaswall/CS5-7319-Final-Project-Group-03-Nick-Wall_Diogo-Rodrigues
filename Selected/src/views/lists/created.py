from Selected.src.views.base import View
from Selected.src.models.lists import List


class CreatedListView(View):
    def __init__(self, created_list: List):
        self.created_list = created_list

    def render(self):
        print("Created list: ")
        print("\t", self.created_list.name)
        print("\t", self.created_list.description)

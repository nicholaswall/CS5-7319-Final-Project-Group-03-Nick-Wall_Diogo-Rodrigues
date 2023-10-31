from mvc.src.views.base import View
from mvc.src.models.lists import List


class CreatedListView(View):
    def __init__(self, created_list: List):
        self.created_list = created_list

    def render(self):
        print("Created list: ", self.created_list)

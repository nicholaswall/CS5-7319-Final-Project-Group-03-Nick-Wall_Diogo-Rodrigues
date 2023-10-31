from mvc.src.views.base import View
from typing import List as ListType
from mvc.src.models.list_tasks import ListTasks


class DisplayListsView(View):
    def __init__(self, lists: ListType[ListTasks]):
        self.lists = lists

    def render(self):
        for list in self.lists:
            print(list.list.name)
            for task in list.tasks:
                description = ": " + str(task.description) if task.description else ""
                print(f"\t{task.title}{description}")

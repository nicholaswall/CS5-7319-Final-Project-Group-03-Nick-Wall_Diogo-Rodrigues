from mvc.src.models.tasks import Task
from mvc.src.views.base import View
from typing import List as ListType


class ChildrenMarkedForDeleteView(View):
    def __init__(self, children_marked_for_delete: ListType[Task]):
        self.children = children_marked_for_delete

    def render(self):
        print("Deleting this task will also delete all of these tasks:")
        for child in self.children:
            print(f"\t{child.title}: {child.description}")

from Selected.src.views.base import View
from Selected.src.models.tasks import Task


class DeletedTaskView(View):
    def __init__(
        self,
        deleted_task: Task,
    ):
        self.deleted_task = deleted_task

    def render(self):
        print("Deleted task: ")
        print("\t", "Name:", self.deleted_task.title)

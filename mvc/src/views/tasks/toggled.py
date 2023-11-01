from mvc.src.views.base import View
from mvc.src.models.tasks import Task


class ToggledTaskView(View):
    def __init__(self, task: Task):
        self.task = task

    def render(self):
        print("Toggled task: ")
        print("\t", "Name:", self.task.title)
        print(
            "\t",
            "Completed:",
            f"{'Yes' if self.task.completed else 'No'} -> {'No' if self.task.completed else 'Yes'}",
        )

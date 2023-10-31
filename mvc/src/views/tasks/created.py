from mvc.src.views.base import View
from mvc.src.models.tasks import Task


class CreatedTaskView(View):
    def __init__(self, created_task: Task):
        self.created_task = created_task

    def render(self):
        print("Created task: ", self.created_task)

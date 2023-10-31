from mvc.src.views.base import View


class CreateTaskPromptView(View):
    def __init__(self):
        pass

    def render(self):
        task_name = input("What is the task's title: ")
        task_description = input("Add a description (optional): ")
        # list_name = input("What list should this task belong to? (optional): ")
        # parent_task_id = input("What is the parent task's title? (optional): ")
        # confirm = input("Confirm task creation? (y/n): ")

        return task_name, task_description

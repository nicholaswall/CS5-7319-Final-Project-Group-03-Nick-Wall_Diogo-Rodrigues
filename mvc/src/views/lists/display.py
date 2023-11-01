from mvc.src.views.base import View
from typing import List as ListType, Dict
from mvc.src.models.list_tasks import ListTasks
from mvc.src.models.tasks import Task

COMPLETED_SYMBOL = "\u2713"
INCOMPLETE_SYMBOL = "X"


class DisplayListsView(View):
    def __init__(self, lists: ListType[ListTasks]):
        self.lists = lists

    def render(self):
        for list in self.lists:
            print(list.list.name)
            children: Dict[int, ListType[Task]] = dict()
            root_tasks: ListType[Task] = []
            # Compute topology
            for task in list.tasks:
                if task.parent_id is not None and task.parent_id not in children:
                    children[task.parent_id] = []

                if task.parent_id is not None:
                    children[task.parent_id].append(task)

                if task.parent_id is None:
                    root_tasks.append(task)

            for task in root_tasks:
                description = ": " + str(task.description) if task.description else ""
                print(
                    f"\t{task.title} [{COMPLETED_SYMBOL if task.completed else INCOMPLETE_SYMBOL}]{description}"
                )

                # Recursively print children
                self.print_children(children, task.id)

    # Recursively print children. This function takesa task id and then checks if that task has children.
    # If it does, it prints them and then calls itself on each child. A tab is used to indent the children.
    def print_children(
        self, children: Dict[int, ListType[Task]], task_id: int, indent: int = 2
    ):
        if task_id not in children:
            return

        for task in children[task_id]:
            description = ": " + str(task.description) if task.description else ""
            tabs = "\t" * indent
            print(
                f"{tabs}{task.title} [{COMPLETED_SYMBOL if task.completed else INCOMPLETE_SYMBOL}]{description}"
            )

            self.print_children(children, task.id, indent + 1)

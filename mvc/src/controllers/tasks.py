from mvc.src.models.lists import ListsModel, List
from mvc.src.models.tasks import TasksModel, Task
from mvc.src.controllers.base import Controller
from mvc.src.views.confirmation_prompt import ConformationPromptView
from mvc.src.views.tasks.children_marked_for_delete import ChildrenMarkedForDeleteView
from mvc.src.views.tasks.create_prompt import CreateTaskPromptView
from typing import Dict, List as ListType, Optional
from mvc.src.views.tasks.created import CreatedTaskView
from mvc.src.views.tasks.delete_prompt import DeleteTaskPromptView
from mvc.src.views.tasks.deleted import DeletedTaskView

from mvc.src.views.tasks.select_list_prompt import SelectListPromptView
from mvc.src.views.tasks.select_parent_task_prompt import SelectParentTaskPromptView


class TasksController(Controller):
    def __init__(self):
        self.lists_model = ListsModel()
        self.tasks_model = TasksModel()

    def create(self):
        view = CreateTaskPromptView()
        title, description = view.render()

        lists: ListType[List] = self.lists_model.get_all()
        if not lists:
            print("You must create a list before creating a task")
            return

        view = SelectListPromptView(lists)
        list_name = view.render()

        selected_list = self.lists_model.get_by_name(list_name)
        tasks = self.tasks_model.get_all_for_list(selected_list.id)

        parent_task_title = None
        parent_task_id = None

        if tasks:
            view = SelectParentTaskPromptView(tasks)
            parent_task_title = view.render()
            if parent_task_title:
                parent_task_id = self.tasks_model.get_by_title(parent_task_title).id

        confirmation = ConformationPromptView().render()
        if not confirmation:
            return

        created_task = self.tasks_model.create(
            title, description, selected_list.id, parent_task_id
        )

        view = CreatedTaskView(created_task, list_name, parent_task_title)
        view.render()

    def delete(self):
        view = DeleteTaskPromptView()
        title = view.render()

        task_to_delete: Optional[Task] = None
        try:
            task_to_delete = self.tasks_model.get_by_title(title)

        # Check if the task has children
        # If it does, delete them
        except Exception:
            print("Task not found")
            return

        children: Dict[int, ListType[Task]] = dict()
        root_tasks: ListType[Task] = []

        # Compute topology
        tasks = self.tasks_model.get_all_for_list(task_to_delete.list_id)
        for task in tasks:
            if task.parent_id is not None and task.parent_id not in children:
                children[task.parent_id] = []

            if task.parent_id is not None:
                children[task.parent_id].append(task)

            if task.parent_id is None:
                root_tasks.append(task)

        def mark_children(children, task_id):
            if task_id not in children:
                return

            for task in children[task_id]:
                to_delete.append(task)
                mark_children(children, task.id)

        # Mark children for deletion
        to_delete: ListType[Task] = []
        for task in root_tasks:
            mark_children(children, task.id)

        view = ChildrenMarkedForDeleteView(to_delete)
        view.render()

        confirmation = ConformationPromptView().render()
        if not confirmation:
            return

        # Delete tasks
        for task in reversed(to_delete):
            self.tasks_model.delete(task.id)
        self.tasks_model.delete(task_to_delete.id)

        view = DeletedTaskView(task_to_delete)
        view.render()

    def update(self):
        pass

    def toggle(self):
        pass

from Selected.src.models.lists import ListsModel, List
from Selected.src.models.tasks import TasksModel, Task
from Selected.src.views.confirmation_prompt import ConformationPromptView
from Selected.src.views.tasks.children_marked_for_delete import (
    ChildrenMarkedForDeleteView,
)
from Selected.src.views.tasks.create_prompt import CreateTaskPromptView
from typing import Dict, List as ListType, Optional, Tuple
from Selected.src.views.tasks.created import CreatedTaskView
from Selected.src.views.tasks.delete_prompt import DeleteTaskPromptView
from Selected.src.views.tasks.deleted import DeletedTaskView
from Selected.src.views.tasks.edit_task_parent_prompt import EditTaskParentPromptView
from Selected.src.views.tasks.edit_task_prompt import EditTaskPromptView
from Selected.src.views.tasks.edited import EditedTaskView

from Selected.src.views.tasks.select_list_prompt import SelectListPromptView
from Selected.src.views.tasks.select_parent_task_prompt import (
    SelectParentTaskPromptView,
)
from Selected.src.views.tasks.toggle_prompt import ToggleTaskPromptView
from Selected.src.views.tasks.toggled import ToggledTaskView


class TasksController:
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

        tasks = self.tasks_model.get_all_for_list(task_to_delete.list_id)
        children, root_tasks = self._compute_topology(tasks)

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

    def edit(self):
        view = EditTaskPromptView()
        intial_name, name, description = view.render()

        # Get all eligible new parents
        task = self.tasks_model.get_by_title(intial_name)
        tasks = self.tasks_model.get_all_for_list(task.list_id)

        children, root_tasks = self._compute_topology(tasks)

        # Remove all child tasks from the list of eligible parents
        # eligible_parents = [task for task in tasks if task not in children[task.id]]
        invalid_parents = []

        def get_children(children, task_id):
            if task_id not in children:
                return

            for task in children[task_id]:
                invalid_parents.append(task)
                get_children(children, task.id)

        get_children(children, task.id)

        invalid_parent_ids = [task.id for task in invalid_parents]
        eligible_parents = [
            t
            for t in tasks
            if task.id not in invalid_parent_ids
            and task.id != t.id
            and t.id != task.parent_id
        ]

        selected_new_parent = None

        if len(eligible_parents) > 0:
            view = EditTaskParentPromptView(eligible_parents)
            selected_new_parent = view.render()

        confirmation = ConformationPromptView().render()
        if not confirmation:
            return

        # Update task
        name = name if name else task.title
        description = description if description else task.description
        selected_new_parent = (
            selected_new_parent if selected_new_parent else task.parent_id
        )

        self.tasks_model.update_name(task.id, name)
        self.tasks_model.update_description(task.id, description)
        self.tasks_model.update_parent(task.id, selected_new_parent)

        edited_task = self.tasks_model.get_by_id(task.id)

        original_task_parent_title = self.tasks_model.get_by_id(task.parent_id).title
        edited_task_parent_title = self.tasks_model.get_by_id(
            edited_task.parent_id
        ).title

        view = EditedTaskView(
            task, original_task_parent_title, edited_task, edited_task_parent_title
        )
        view.render()

    def toggle_completion(self):
        view = ToggleTaskPromptView()
        title = view.render()

        task = self.tasks_model.get_by_title(title)

        confirmation = ConformationPromptView().render()
        if not confirmation:
            return

        self.tasks_model.toggle_completed(task.id)

        view = ToggledTaskView(task)
        view.render()

    def _compute_topology(
        self, tasks: ListType[Task]
    ) -> Tuple[Dict[int, ListType[Task]], ListType[Task]]:
        children: Dict[int, ListType[Task]] = dict()
        root_tasks: ListType[Task] = []

        # Compute topology
        for task in tasks:
            if task.parent_id is not None and task.parent_id not in children:
                children[task.parent_id] = []

            if task.parent_id is not None:
                children[task.parent_id].append(task)

            if task.parent_id is None:
                root_tasks.append(task)

        return children, root_tasks

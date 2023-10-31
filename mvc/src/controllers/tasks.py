from mvc.src.models.lists import ListsModel, List
from mvc.src.models.tasks import TasksModel
from mvc.src.controllers.base import Controller
from mvc.src.views.tasks.create_prompt import CreateTaskPromptView
from typing import List as ListType
from mvc.src.views.tasks.created import CreatedTaskView

from mvc.src.views.tasks.select_list_prompt import SelectListPromptView
from mvc.src.views.tasks.select_parent_task_prompt import SelectParentTaskPromptView


class TasksController(Controller):
    def __init__(self):
        self.lists_model = ListsModel()
        self.tasks_model = TasksModel()

    def create(self):
        view = CreateTaskPromptView()
        name, description = view.render()

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
            parent_task_id = self.tasks_model.get_by_title(parent_task_title).id

        created_task = self.tasks_model.create(
            name, description, selected_list.id, parent_task_id
        )

        view = CreatedTaskView(created_task)
        view.render()

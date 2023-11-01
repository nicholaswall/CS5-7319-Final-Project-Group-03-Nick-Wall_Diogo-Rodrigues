from mvc.src.models.lists import ListsModel, List
from mvc.src.models.tasks import TasksModel
from mvc.src.controllers.base import Controller
from mvc.src.views.confirmation_prompt import ConformationPromptView
from mvc.src.views.lists.create_prompt import CreateListPromptView
from mvc.src.views.lists.created import CreatedListView
from mvc.src.views.lists.display_prompt import DisplayListPromptView
from mvc.src.views.lists.display import DisplayListsView
from typing import List as ListType
from mvc.src.models.list_tasks import ListTasks


class ListsController(Controller):
    def __init__(self):
        self.lists_model = ListsModel()
        self.tasks_model = TasksModel()

    def create(self):
        view = CreateListPromptView()
        name, description = view.render()
        confirmation = ConformationPromptView().render()
        if not confirmation:
            return
        created_list: List = self.lists_model.create(name, description)
        view = CreatedListView(created_list)
        view.render()

    def display(self):
        view = DisplayListPromptView()
        filter = view.render()
        lists: ListType[List] = self.lists_model.get_all()
        if filter:
            lists = [list for list in lists if filter in list.name]
        lists_tasks: ListType[ListTasks] = [
            ListTasks(list, self.tasks_model.get_all_for_list(list.id))
            for list in lists
        ]
        view = DisplayListsView(lists_tasks)
        view.render()

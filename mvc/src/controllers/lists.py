from mvc.src.models.lists import ListsModel, List
from mvc.src.models.tasks import TasksModel
from mvc.src.controllers.base import Controller
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
        name, _ = view.render()
        created_list: List = self.lists_model.create(name)
        view = CreatedListView(created_list)
        view.render()

    def display(self):
        view = DisplayListPromptView()
        filter = view.render()
        lists: ListType[List] = self.lists_model.get_all()
        print("got lists", lists)
        if filter != "":
            print("filtering lists", filter)
            lists = [list for list in lists if list.name == filter]
        lists_tasks: ListType[ListTasks] = [
            ListTasks(list, self.tasks_model.get_all_for_list(list.id))
            for list in lists
        ]

        print("got lists_tasks", lists_tasks)

        view = DisplayListsView(lists_tasks)
        view.render()

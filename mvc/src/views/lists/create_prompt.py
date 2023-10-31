from mvc.src.views.base import View


class CreateListPromptView(View):
    def render(self):
        list_name = input("Enter a name for your list: ")
        # TODO: update list to have a description
        list_description = input("Enter a description for your list: ")
        return list_name, list_description

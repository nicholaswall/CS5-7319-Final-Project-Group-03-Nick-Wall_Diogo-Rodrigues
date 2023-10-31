from mvc.src.views.base import View


class DisplayListPromptView(View):
    def render(self):
        list_name = input("Filter lists by name (leave empty for all): ")
        return list_name

from argparse import ArgumentParser
from mvc.src.controllers.lists import ListsController
from mvc.src.controllers.tasks import TasksController


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="mvc", description="A simple todo list app", epilog="Thanks for using mvc!"
    )

    sub_parsers = parser.add_subparsers(help="sub-command help", dest="command")

    # List parsers
    list_parser = sub_parsers.add_parser("list")
    list_sub_parsers = list_parser.add_subparsers(
        help="Manage and view lists", dest="list_command"
    )

    # Create lists
    create_list_parser = list_sub_parsers.add_parser("create", help="Create a new list")
    # create_list_parser.add_argument("name", type=str, help="list name")

    # Get lists
    display_lists_parser = list_sub_parsers.add_parser(
        "display", help="Display all lists"
    )
    # display_lists_parser.add_argument("--name", help="list name")

    # Tasks parsers
    task_parser = sub_parsers.add_parser("task")
    task_sub_parsers = task_parser.add_subparsers(
        help="Manage and view tasks", dest="task_command"
    )

    # Create tasks
    create_task_parser = task_sub_parsers.add_parser("create", help="Create a new task")

    # Edit tasks
    edit_task_parser = task_sub_parsers.add_parser("edit", help="Edit a task")

    # Delete tasks
    delete_task_parser = task_sub_parsers.add_parser("delete", help="Delete a task")

    # Toggle task completion
    toggle_task_parser = task_sub_parsers.add_parser(
        "complete", help="Toggle task completion"
    )

    args = parser.parse_args()
    sub_parser_name = args.command

    if sub_parser_name == "list":
        list_command = args.list_command
        if list_command == "create":
            ListsController().create()
        elif list_command == "display":
            ListsController().display()
    elif sub_parser_name == "task":
        task_command = args.task_command
        if task_command == "create":
            TasksController().create()
        elif task_command == "edit":
            TasksController().edit()
        elif task_command == "delete":
            TasksController().delete()
        elif task_command == "complete":
            TasksController().toggle_completion()

    # print("Hello world from mvc")
    # created_list = ListsModel().create("test")
    # print("Created list: ", created_list)
    # lists = ListsModel().get_all()
    # print("Lists: ", lists)

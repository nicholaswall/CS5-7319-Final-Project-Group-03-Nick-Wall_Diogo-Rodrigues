from argparse import ArgumentParser
from Unselected.src.utils import (
    LIST_TABLE_NAME,
    TASK_TABLE_NAME,
    CURSOR,
    TaskList,
    Task,
    set_up_db,
)
from Unselected.src.db import con, sql_value
from typing import Dict, List as ListType


class Pipe:
    def __init__(self, functions):
        self.functions = functions

    def __call__(self, x):
        input_ = x
        for function in self.functions:
            temp_result = function(input_)
            input_ = temp_result

        return input_


class Command:
    def __init__(self):
        self.my_pipe = Pipe([])

    def execute(self):
        raise NotImplementedError

    def get_lists(self, list_name: str = None):
        """
        Get all lists from the database
        """
        # Select only one specific list
        if list_name:
            sql = f"SELECT * FROM '{LIST_TABLE_NAME}' WHERE name = '{list_name}'"
            lists = CURSOR.execute(sql).fetchall()
            con.commit()
        # Select all lists
        else:
            sql = f"SELECT * FROM '{LIST_TABLE_NAME}'"
            lists = CURSOR.execute(sql).fetchall()
            con.commit()
        return [
            TaskList(id=list[0], name=list[1], description=list[2]) for list in lists
        ]

    def display_list(self, list: TaskList):
        """
        Display a list and its description, if available
        """
        if list:
            print(" List: " + list.name)
            if list.description != "NULL":
                print(" Description: " + list.description + "\n")
            else:
                print(" Description: N/A\n")
        else:
            print("This list does not exist!")

    def get_ids(self, task: Task):
        """
        Get the id of a task and its list based on their names
        """
        sql = f"SELECT id FROM '{LIST_TABLE_NAME}' WHERE name = '{task.list_name}'"
        task.list_id = CURSOR.execute(sql).fetchone()[0]
        sql = f"SELECT id FROM '{TASK_TABLE_NAME}' WHERE title = '{task.title}' AND list_id = {task.list_id}"
        task.id = CURSOR.execute(sql).fetchone()[0]
        con.commit()

        return task.id


class ViewTasksCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe(
            [self.get_lists, self.get_tasks_for_lists, self.print_super_tasks]
        )

    def execute(self, list_name=None):
        self.my_pipe(list_name)

    def get_tasks_for_lists(self, lists: ListType[TaskList]):
        """
        Get all tasks for given lists
        """
        list_and_super_tasks = {}
        for list in lists:
            # Get super tasks
            sql = f"SELECT * FROM '{TASK_TABLE_NAME}' WHERE list_id = {list.id} AND parent_id = 'NULL'"
            super_tasks = CURSOR.execute(sql).fetchall()
            con.commit()

            super_tasks = [
                Task(
                    id=task[0],
                    title=task[1],
                    description=task[2],
                    completed=task[3],
                    list_id=task[4],
                    parent_id=task[5],
                )
                for task in super_tasks
            ]
            list_and_super_tasks[list.name] = [
                super_task.id for super_task in super_tasks
            ]

        return list_and_super_tasks

    def print_super_tasks(self, list_and_super_tasks: Dict[str, ListType[int]]):
        """
        Print all sub tasks of a task recursively
        """
        for list_name in list_and_super_tasks:
            print(f"{list_name}:")
            for super_id in list_and_super_tasks[list_name]:
                sql = f"SELECT title, description FROM '{TASK_TABLE_NAME}' WHERE id = {super_id}"
                super_task_name = CURSOR.execute(sql).fetchone()[0]
                super_task_description = CURSOR.execute(sql).fetchone()[1]
                if super_task_description:
                    print(f"- {super_task_name}: {super_task_description}")
                else:
                    print(f"- {super_task_name}")
                self.print_sub_tasks(super_id)

    def print_sub_tasks(self, super_id: int, counter: int = 2):
        """
        Print all sub tasks of a task recursively
        """
        sql = f"SELECT id, title, description FROM '{TASK_TABLE_NAME}' WHERE parent_id = {super_id}"
        sub_tasks = CURSOR.execute(sql).fetchall()
        # print(sub_tasks)
        for sub_task in sub_tasks:
            # Print dashes
            for _ in range(counter):
                print("-", end="")
            if sub_task[2]:
                print(f" {sub_task[1]}: {sub_task[2]}")
            else:
                print(f" {sub_task[1]}")
            self.print_sub_tasks(sub_task[0], counter + 1)


class ViewListsCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe([self.get_lists, self.display_lists])

    def execute(self, list_name=None):
        self.my_pipe(list_name)

    def display_lists(self, lists: ListType[TaskList]):
        """
        Display all lists and their descriptions, if available
        """
        print("All Lists:")
        for list in lists:
            self.display_list(list)


class CreateListCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe(
            [self.create_list, self.confirm_list_creation, self.display_list]
        )

    def execute(self, list: TaskList):
        self.my_pipe(list)

    def create_list(self, task_list: TaskList):
        """
        Create a new list
        """
        # If no description is given, set it to NULL
        if not task_list.description:
            task_list.description = "NULL"
        sql = (
            "INSERT INTO "
            + LIST_TABLE_NAME
            + " (name, description) VALUES "
            + sql_value([task_list.name, task_list.description])
            + " RETURNING *"
        )
        created_list = CURSOR.execute(sql).fetchone()
        con.commit()

        id = created_list[0]

        return id

    def confirm_list_creation(self, id: int):
        """
        Confirm that a list was created and exists in the database
        """
        sql = f"SELECT * FROM '{LIST_TABLE_NAME}' WHERE id = {id}"
        created_list = CURSOR.execute(sql).fetchone()
        con.commit()

        if created_list:
            print("Successfully created List!")
            return TaskList(
                id=created_list[0], name=created_list[1], description=created_list[2]
            )
        print("Failed to create List...")
        return None


class CreateTaskCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe(
            [self.create_task, self.confirm_task_creation, self.display_task]
        )

    def execute(self, list: TaskList):
        self.my_pipe(list)

    def create_task(self, task: Task):
        """
        Create a new task
        """
        # Get list id from list name
        sql = f"SELECT id FROM '{LIST_TABLE_NAME}' WHERE name = '{task.list_name}'"
        list_id = CURSOR.execute(sql).fetchone()[0]

        # If parent name is given, get its id
        if task.parent_name:
            sql = (
                f"SELECT id FROM '{TASK_TABLE_NAME}' WHERE title = '{task.parent_name}'"
            )
            parent_id = CURSOR.execute(sql).fetchone()[0]
        else:
            parent_id = "NULL"

        # If no description is given, leave it blank
        if not task.description:
            sql = (
                "INSERT INTO "
                + TASK_TABLE_NAME
                + " (title, list_id, parent_id) VALUES "
                + sql_value([task.title, list_id, parent_id])
                + " RETURNING *"
            )
        else:
            sql = (
                "INSERT INTO "
                + TASK_TABLE_NAME
                + " (title, description, list_id, parent_id) VALUES "
                + sql_value([task.title, task.description, list_id, parent_id])
                + " RETURNING *"
            )
        created_task = CURSOR.execute(sql).fetchone()
        con.commit()

        return Task(
            id=created_task[0],
            title=created_task[1],
            description=created_task[2],
            completed=created_task[3],
            list_id=created_task[4],
            parent_id=created_task[5],
            list_name=task.list_name,
            parent_name=task.parent_name,
        )

    def confirm_task_creation(self, task: Task):
        """
        Confirm that a task was created and exists in the database
        """
        sql = f"SELECT * FROM '{TASK_TABLE_NAME}' WHERE id = {task.id}"
        created_task = CURSOR.execute(sql).fetchone()
        con.commit()

        if created_task:
            print("Successfully created Task!")
            return task
        print("Failed to create Task...")
        return Task()

    def display_task(self, task: Task):
        """
        Display a task that was created
        """
        if task:
            print("Task: " + task.title)
            if task.description:
                print("Description: " + task.description)
            else:
                print("Description: N/A")
            if task.completed:
                print("Completed: Yes")
            else:
                print("Completed: No")
            print("List Name: " + str(task.list_name))
            if task.parent_name:
                print("Parent Name: " + str(task.parent_name))
            else:
                print("Parent Name: N/A")
            print()


class DeleteTaskCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe(
            [
                self.get_ids,
                self.delete_task,
                self.delete_substasks,
                self.confirm_task_deletion,
            ]
        )

    def execute(self, list: TaskList):
        self.my_pipe(list)

    def delete_task(self, task_id: int):
        """
        Delete a task
        """
        sql = f"DELETE FROM {TASK_TABLE_NAME} WHERE id = {task_id}"
        CURSOR.execute(sql)
        con.commit()

        return task_id

    def delete_substasks(self, task_id: int):
        """
        Delete all substasks of a task
        """
        # Get substasks for given task
        sql = f"SELECT id FROM {TASK_TABLE_NAME} WHERE parent_id = {task_id}"
        subtasks = CURSOR.execute(sql).fetchall()
        con.commit()
        # Recursively delete substasks
        for subtask in subtasks:
            self.delete_substasks(subtask[0])
        # Delete given task
        sql = f"DELETE FROM {TASK_TABLE_NAME} WHERE id = '{task_id}'"
        CURSOR.execute(sql)
        con.commit()
        return task_id

    def confirm_task_deletion(self, task_id: int):
        """
        Confirm that a task was deleted and does not exist in the database
        """
        sql = f"SELECT * FROM {TASK_TABLE_NAME} WHERE id = '{task_id}'"
        deleted_task = CURSOR.execute(sql).fetchall()
        con.commit()

        if not deleted_task:
            print("Successfully deleted Task!")
        else:
            print("Failed to delete Task...")


class DeleteListCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe(
            [
                self.get_list_id,
                self.delete_list,
                self.delete_tasks_from_list,
                self.confirm_list_deletion,
            ]
        )

    def execute(self, list: TaskList):
        self.my_pipe(list)

    def get_list_id(self, list: TaskList):
        """
        Get the id of a list based on its name
        """
        sql = f"SELECT id FROM '{LIST_TABLE_NAME}' WHERE name = '{list.name}'"
        id = CURSOR.execute(sql).fetchone()[0]
        con.commit()

        return id

    def delete_list(self, id: int):
        """
        Delete a list
        """
        sql = f"DELETE FROM {LIST_TABLE_NAME} WHERE id = {id}"
        CURSOR.execute(sql)
        con.commit()

        return id

    def delete_tasks_from_list(self, id: int):
        """
        Delete all tasks from the database that belonged to a deleted list
        """
        sql = f"DELETE FROM {TASK_TABLE_NAME} WHERE list_id = {id}"
        CURSOR.execute(sql)
        con.commit()

        return id

    def confirm_list_deletion(self, id: int):
        """
        Confirm that a list was deleted and does not exist in the database
        """
        sql = f"SELECT * FROM {LIST_TABLE_NAME} WHERE id = {id}"
        deleted_list = CURSOR.execute(sql).fetchall()
        con.commit()

        if not deleted_list:
            print("Successfully deleted List!")
        else:
            print("Failed to delete List...")


class EditTaskCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe([self.edit_task, self.confirm_task_changes])

    def execute(self, tasks: Dict[str, Task]):
        self.my_pipe(tasks)

    def edit_task(self, tasks: Dict[str, Task]):
        """
        Edit a task - title, description, or parent
        """
        orig_task = tasks["orig_task"]
        new_task = tasks["new_task"]

        orig_task.id = self.get_ids(orig_task)
        new_task.id = orig_task.id

        sql = f"UPDATE {TASK_TABLE_NAME} SET "

        # Update the task's title, description, and/or parent based on given input
        if new_task.title:
            sql += f"title = '{new_task.title}', "
        else:
            new_task.title = orig_task.title
        if new_task.description:
            sql += f"description = '{new_task.description}', "
        if new_task.parent_name:
            parent_id_sql = f"SELECT id FROM {TASK_TABLE_NAME} WHERE title = '{new_task.parent_name}'"
            new_task.parent_id = CURSOR.execute(parent_id_sql).fetchone()[0]
            sql += f"parent_id = {new_task.parent_id}, "

        # Remove ', ' and add WHERE clause
        sql = sql[:-2] + f" WHERE id = {new_task.id}"

        CURSOR.execute(sql)
        con.commit()

        return new_task

    def confirm_task_changes(self, new_task: Task):
        """
        Confirm that a task was edited and exists in the database
        """
        sql = f"SELECT * FROM {TASK_TABLE_NAME} WHERE id = {new_task.id}"
        edited_task = CURSOR.execute(sql).fetchone()
        con.commit()
        edited_task = Task(
            id=edited_task[0],
            title=edited_task[1],
            description=edited_task[2],
            completed=edited_task[3],
            list_id=edited_task[4],
            parent_id=edited_task[5],
        )

        if edited_task == new_task:
            print("Successfully edited Task!")
        else:
            print("Failed to edit Task...")


class ToggleTaskCommand(Command):
    def __init__(self):
        super().__init__()
        self.my_pipe = Pipe([self.toggle_task, self.confirm_task_toggle])

    def execute(self, task_name: str):
        self.my_pipe(task_name)

    def toggle_task(self, task_name: str):
        """
        Toggle a task's completed value
        """
        sql = f"SELECT id, completed FROM {TASK_TABLE_NAME} WHERE title = '{task_name}'"
        task_data = CURSOR.execute(sql).fetchone()
        con.commit()
        task_id = task_data[0]
        orig_completed_val = task_data[1]
        # If the task is already completed, set it to incomplete
        if orig_completed_val:
            sql = f"UPDATE {TASK_TABLE_NAME} SET completed = 0 WHERE id = {task_id}"
            CURSOR.execute(sql)
            con.commit()
            return [task_id, 0]
        # Else, set it to completed
        sql = f"UPDATE {TASK_TABLE_NAME} SET completed = 1 WHERE id = {task_id}"
        CURSOR.execute(sql)
        con.commit()
        return [task_id, 1]

    def confirm_task_toggle(self, id_and_completed_status: ListType[int]):
        """
        Confirm that a task's completed value was toggled
        """
        task_id = id_and_completed_status[0]
        toggled_completed_val = id_and_completed_status[1]

        sql = f"SELECT completed FROM {TASK_TABLE_NAME} WHERE id = {task_id}"
        completed_val = CURSOR.execute(sql).fetchone()[0]

        if completed_val == toggled_completed_val:
            print("Successfully toggled Task!")
        else:
            print("Failed to toggle Task...")


if __name__ == "__main__":
    set_up_db()
    parser = ArgumentParser(
        prog="pipe_filter",
        description="A simple todo list app",
        epilog="Thanks for using pipe_filter!",
    )

    sub_parsers = parser.add_subparsers(help="sub-command help", dest="command")

    # List parsers
    list_parser = sub_parsers.add_parser("list")
    list_sub_parsers = list_parser.add_subparsers(
        help="Manage and view lists", dest="list_command"
    )

    # Create lists
    create_list_parser = list_sub_parsers.add_parser("create", help="Create a new list")
    create_list_parser.add_argument("name", type=str, help="list name")
    create_list_parser.add_argument(
        "description", type=str, help="list description", nargs="?"
    )

    # Delete lists
    delete_list_parser = list_sub_parsers.add_parser("delete", help="Delete a list")
    delete_list_parser.add_argument("name", type=str, help="list name")

    # View lists
    view_lists_parser = list_sub_parsers.add_parser("view", help="View a list")
    view_lists_parser.add_argument(
        "name", help="View a specific list (optional)", nargs="?"
    )

    # Task parsers
    task_parser = sub_parsers.add_parser("task")
    task_sub_parsers = task_parser.add_subparsers(
        help="Manage and view tasks", dest="task_command"
    )

    # Create tasks
    create_task_parser = task_sub_parsers.add_parser("create", help="Create a new task")
    create_task_parser.add_argument("--title", "-t", help="task name")
    create_task_parser.add_argument("--list_name", "-ln", help="list name")
    create_task_parser.add_argument(
        "--parent_name", "-pn", help="parent task name", nargs="?"
    )
    create_task_parser.add_argument(
        "--description", "-d", help="task description", nargs="?"
    )

    # Delete tasks
    delete_task_parser = task_sub_parsers.add_parser("delete", help="Delete a task")
    delete_task_parser.add_argument("title", type=str, help="task name")
    delete_task_parser.add_argument("list_name", type=str, help="list name")

    # View tasks
    view_tasks_parser = task_sub_parsers.add_parser(
        "view", help="View all tasks from all or a specific list"
    )
    view_tasks_parser.add_argument(
        "list_name", help="View a specific list (optional)", nargs="?"
    )

    # Edit tasks
    edit_task_parser = task_sub_parsers.add_parser("edit", help="Edit a task")
    edit_task_parser.add_argument(
        "--orig_title", "-ot", type=str, help="original task name"
    )
    edit_task_parser.add_argument(
        "--list_name", "-ln", type=str, help="original list name"
    )
    edit_task_parser.add_argument(
        "--new_title", "-nt", type=str, help="new task name", nargs="?"
    )
    edit_task_parser.add_argument(
        "--new_parent_name", "-npn", type=str, help="new parent task name", nargs="?"
    )
    edit_task_parser.add_argument(
        "--new_description", "-nd", type=str, help="new task description", nargs="?"
    )

    # Toggle tasks
    toggle_task_parser = task_sub_parsers.add_parser("toggle", help="Toggle a task")
    toggle_task_parser.add_argument("title", type=str, help="task name")

    args = parser.parse_args()
    sub_parser_name = args.command

    if sub_parser_name == "list":
        list_command = args.list_command
        if list_command == "create":
            CreateListCommand().execute(
                TaskList(name=args.name, description=args.description)
            )
        elif list_command == "delete":
            DeleteListCommand().execute(TaskList(args.name))
        elif list_command == "view":
            ViewListsCommand().execute(args.name)
    elif sub_parser_name == "task":
        list_command = args.task_command
        if list_command == "create":
            CreateTaskCommand().execute(
                Task(
                    title=args.title,
                    list_name=args.list_name,
                    parent_name=args.parent_name,
                    description=args.description,
                )
            )
        elif list_command == "delete":
            DeleteTaskCommand().execute(
                Task(title=args.title, list_name=args.list_name)
            )
        elif list_command == "view":
            ViewTasksCommand().execute(args.list_name)
        elif list_command == "edit":
            EditTaskCommand().execute(
                {
                    "orig_task": Task(title=args.orig_title, list_name=args.list_name),
                    "new_task": Task(
                        title=args.new_title,
                        parent_name=args.new_parent_name,
                        description=args.new_description,
                    ),
                }
            )
        elif list_command == "toggle":
            ToggleTaskCommand().execute(args.title)

from Selected.src.db import con, sql_value
from dataclasses import dataclass
from typing import List as ListType, Optional


@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    list_id: int
    parent_id: Optional[int]

    def __post_init__(self):
        if self.parent_id == "NULL":
            self.parent_id = None


class TasksModel:
    def __init__(self):
        self.cursor = con.cursor()
        self.table_name = "tasks"

        sql = (
            "CREATE TABLE IF NOT EXISTS "
            + self.table_name
            + """ (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT NOT NULL, 
                description TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE,
                list_id INTEGER NOT NULL,
                parent_id INTEGER,
                FOREIGN KEY(list_id) REFERENCES lists(id),
                FOREIGN KEY(parent_id) REFERENCES tasks(id)
                   )
            """
        )
        self.cursor.execute(sql)

    def create(
        self,
        title: str,
        description: Optional[str],
        list_id: int,
        parent_id: Optional[int],
    ) -> Task:
        if not parent_id:
            parent_id = "NULL"

        if not description:
            description = ""

        sql = (
            "INSERT INTO "
            + self.table_name
            + " (title, description, list_id, parent_id) VALUES "
            + sql_value([title, description, list_id, parent_id])
            + " RETURNING *"
        )
        created_task = self.cursor.execute(sql).fetchone()
        con.commit()

        return Task(*created_task)

    def get_all_for_list(self, list_id: int) -> ListType[Task]:
        sql = "SELECT * FROM " + self.table_name + " WHERE list_id = " + str(list_id)
        tasks = self.cursor.execute(sql).fetchall()
        con.commit()

        return [Task(*task) for task in tasks]

    def get_by_id(self, id: int) -> Task:
        sql = "SELECT * FROM " + self.table_name + " WHERE id = " + str(id)
        task = self.cursor.execute(sql).fetchone()
        con.commit()

        if not task:
            raise ValueError("No task with that id")

        return Task(*task)

    def get_by_title(self, title: str) -> Task:
        sql = "SELECT * FROM " + self.table_name + " WHERE title = '" + title + "'"
        task = self.cursor.execute(sql).fetchone()
        con.commit()

        if not task:
            raise ValueError("No task with that title")

        return Task(*task)

    def delete(self, id: int) -> None:
        sql = "DELETE FROM " + self.table_name + " WHERE id = " + str(id)
        self.cursor.execute(sql)
        con.commit()

    def update_name(self, id: int, title: str) -> None:
        sql = (
            "UPDATE "
            + self.table_name
            + " SET title = '"
            + title
            + "' WHERE id = "
            + str(id)
        )
        self.cursor.execute(sql)
        con.commit()

    def update_description(self, id: int, description: str) -> None:
        sql = (
            "UPDATE "
            + self.table_name
            + " SET description = '"
            + description
            + "' WHERE id = "
            + str(id)
        )
        self.cursor.execute(sql)
        con.commit()

    def update_parent(self, id: int, parent_id: int) -> None:
        sql = (
            "UPDATE "
            + self.table_name
            + " SET parent_id = "
            + str(parent_id)
            + " WHERE id = "
            + str(id)
        )
        self.cursor.execute(sql)
        con.commit()

    def toggle_completed(self, id: int) -> None:
        sql = (
            "UPDATE "
            + self.table_name
            + " SET completed = NOT completed WHERE id = "
            + str(id)
        )
        self.cursor.execute(sql)
        con.commit()

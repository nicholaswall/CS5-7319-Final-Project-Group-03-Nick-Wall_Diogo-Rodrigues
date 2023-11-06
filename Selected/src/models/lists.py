from Selected.src.db import con, sql_value
from dataclasses import dataclass
from typing import List as ListType, Optional


@dataclass
class List:
    id: int
    name: str
    description: str


class ListsModel:
    def __init__(self):
        self.cursor = con.cursor()
        self.table_name = "lists"

        sql = (
            "CREATE TABLE IF NOT EXISTS "
            + self.table_name
            + " (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL)"
        )
        self.cursor.execute(sql)

    def create(self, name: str, description: Optional[str]) -> List:
        if not description:
            description = ""

        sql = (
            "INSERT INTO "
            + self.table_name
            + " (name, description) VALUES "
            + sql_value([name, description])
            + " RETURNING *"
        )
        created_list = self.cursor.execute(sql).fetchone()
        con.commit()

        return List(*created_list)

    def get_all(self) -> ListType[List]:
        sql = "SELECT * FROM " + self.table_name
        lists = self.cursor.execute(sql).fetchall()
        con.commit()

        return [List(*list) for list in lists]

    def get_by_id(self, id: int) -> List:
        sql = "SELECT * FROM " + self.table_name + " WHERE id = " + str(id)
        list = self.cursor.execute(sql).fetchone()
        con.commit()

        return List(*list)

    def get_by_name(self, name: str) -> List:
        sql = "SELECT * FROM " + self.table_name + " WHERE name = '" + name + "'"
        list = self.cursor.execute(sql).fetchone()
        con.commit()

        return List(*list)

    def delete(self, id: int) -> None:
        sql = "DELETE FROM " + self.table_name + " WHERE id = " + str(id)
        self.cursor.execute(sql)
        con.commit()

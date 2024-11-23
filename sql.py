import sqlite3
from datetime import datetime
from contextlib import closing


class Tasks:
    """Класс для работы с sql

    Raises:
        IndexError: возвращает ошибку при несуществующем индексе
    """

    priority_dict: dict = {1: "низкий",
                           2: "нормальный",
                           3: "высокий"}
    status_dict: dict = {1: "не начата",
                         2: "в работе",
                         3: "выполнена",
                         4: "просрочена"}
    db_path: str = "tasks.db"

    def create_task(name: str,
                    priority: int,
                    description: str,
                    deadline: datetime):

        create_time: datetime = datetime.now().strftime("%d-%m-%Y %H:%M")
        status: int = 1

        sql_query = """INSERT INTO tasks\
            (name,description,priority,status,create_time,deadline) \
                VALUES(?,?,?,?,?,?)"""
        try:
            priority = int(priority)

            if priority not in range(1, 4):
                raise IndexError("Приоритет должен быть от 1 до 3")
            else:
                priority = Tasks.priority_dict[priority]

        except Exception as ex:
            return f"Ошибка:{ex}"

        if len(deadline) == 0:
            deadline = "NULL"
        else:
            try:
                deadline = datetime.strptime(deadline,
                                             "%d-%m-%Y %H:%M"
                                             ).strftime(
                                                 "%d-%m-%Y %H:%M")

            except Exception:
                return "Ошибка: Неверная дата"

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:
                    data = (
                        name,
                        description,
                        priority,
                        Tasks.status_dict[status],
                        create_time,
                        deadline,
                    )

                    cursor.execute(sql_query, data)

                    conn.commit()

                    return "Задача создана"

        except Exception as ex:
            return f"Ошибка:{ex}"

    def search_task(search_string):

        sql_query = f'select * from tasks where \
            id || name || description || priority || create_time || deadline \
                like "%{search_string}%"'

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:

                    query = cursor.execute(sql_query)
                    return query.fetchall()

        except Exception as ex:
            return f"Ошибка:{ex}"

    def delete_task(index_to_delete):

        sql_query = f"DELETE FROM tasks WHERE id = {index_to_delete}"

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:

                    if (
                        cursor.execute(
                            f"SELECT EXISTS (SELECT * FROM tasks\
                            WHERE id = {index_to_delete})"
                        ).fetchone()[0]
                        != 0
                    ):

                        cursor.execute(sql_query)
                        conn.commit()

                        return "Запись удалена"

                    else:
                        raise IndexError("Нет такой записи")

        except Exception as ex:
            return f"Ошибка:{ex}"

    def update_task(task_index, task_key, new_value):

        try:
            if task_key == "Priority":
                new_value = int(new_value)
                if new_value not in range(1, 4):
                    raise IndexError("Приоритет должен быть от 1 до 3")
                else:
                    new_value = Tasks.priority_dict[new_value]

            elif task_key == "Status":
                new_value = int(new_value)
                new_value = Tasks.status_dict[new_value]
        except Exception as ex:
            return f"Ошибка:{ex}"

        sql_query = (
            f'UPDATE tasks SET "{task_key}" = "{new_value}"\
            WHERE id = {task_index}'
        )

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:

                    if (
                        cursor.execute(
                            f"SELECT EXISTS (SELECT * FROM tasks\
                                WHERE id = {task_index})"
                        ).fetchone()[0]
                        != 0
                    ):

                        cursor.execute(sql_query)
                        conn.commit()

                        return "Запись обновлена"

                    else:
                        raise IndexError("Нет такой записи")

        except Exception as ex:
            return f"Ошибка:{ex}"

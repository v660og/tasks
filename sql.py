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
                    deadline: datetime) -> str:
        """Создает задачу

        Args:
            name (str): Имя задачи
            priority (int): Приоритет
            description (str): Описание
            deadline (datatime): Срок

        Returns:
            str: статус выполнения
        """
        create_time: datetime = datetime.now().strftime("%d-%m-%Y %H:%M")
        status: int = 1

        sql_query: str = """INSERT INTO tasks\
            (name,description,priority,status,create_time,deadline) \
                VALUES(?,?,?,?,?,?)"""
        try:
            priority: int = int(priority)

            if priority not in range(1, 4):
                raise IndexError("Приоритет должен быть от 1 до 3")
            else:
                priority = Tasks.priority_dict[priority]

        except Exception as ex:
            return f"Ошибка:{ex}"

        if len(deadline) == 0:
            deadline: str = "NULL"
        else:
            try:
                deadline: datetime = datetime.strptime(
                    deadline,
                    "%d-%m-%Y %H:%M"
                    ).strftime(
                    "%d-%m-%Y %H:%M"
                    )

            except Exception:
                return "Ошибка: Неверная дата"

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:
                    data: tuple = (
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

    def search_task(search_string: str, task_key: str = ''):
        """поиск задач в БД

        Args:
            search_string (str): строка поиска
            task_key (str): ключ. По умолчанию ''.

        Returns:
            list: Список задач
        """
        if len(task_key) == 0:
            task_key: str = 'id || name || description ||\
                priority || create_time || deadline'

        sql_query: str = f'select * from tasks where \
            {task_key} like "%{search_string}%"'

        try:
            with closing(sqlite3.connect(Tasks.db_path)) as conn:
                with closing(conn.cursor()) as cursor:

                    query: str = cursor.execute(sql_query)
                    return query.fetchall()

        except Exception as ex:
            return f"Ошибка:{ex}"

    def delete_task(index_to_delete: int) -> str:
        """Удаляет задачи по индексу

        Args:
            index_to_delete (int): Индекс

        Raises:
            IndexError: Ошибка индекса

        Returns:
            str: статус
        """
        sql_query: str = f"DELETE FROM tasks WHERE id = {index_to_delete}"

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

    def update_task(task_index: int, task_key: str, new_value: str) -> str:
        """Обновление задачи

        Args:
            task_index (int): Индекс
            task_key (str): Ключ
            new_value (str): Новое значение

        Raises:
            IndexError: Ошибка индекса

        Returns:
            str: статус
        """
        try:
            if task_key == "Priority":
                new_value: int = int(new_value)
                if new_value not in range(1, 4):
                    raise IndexError("Приоритет должен быть от 1 до 3")
                else:
                    new_value: int = Tasks.priority_dict[new_value]

            elif task_key == "Status":
                new_value: int = int(new_value)
                new_value: int = Tasks.status_dict[new_value]
        except Exception as ex:
            return f"Ошибка:{ex}"

        sql_query: str = (
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

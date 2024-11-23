import sqlite3
from contextlib import closing

def create_table():
    try:

        with closing(sqlite3.connect("tasks.db")) as conn:
            with closing(conn.cursor()) as cursor:

                cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                priority INTEGER NOT NULL,
                status INTEGER NOT NULL,
                create_time TEXT NOT NULL,
                deadline TEXT
                )
                """
                )

                conn.commit()


    except Exception as ex:
        print(ex)

import sys
sys.path.append('УКАЖИТЕ ПУТЬ К ПАПКЕ с main')
import time
import os.path
import db
import sql


def test_db():
    db.create_table("test.db")
    assert os.path.exists("./test.db")


def test_row_create():
    sql.Tasks.db_path = "test.db"
    create_task = sql.Tasks.create_task("test", 1, "test", "01-01-1970 00:00")
    assert create_task == "Задача создана"


def test_row_get():
    sql.Tasks.db_path = "test.db"
    row = sql.Tasks.search_task("test")
    assert row[0][1] == "test"


def test_row_update():
    sql.Tasks.db_path = "test.db"
    row = sql.Tasks.update_task(1, "Priority", 2)
    assert row == "Запись обновлена"


def test_row_delete():
    sql.Tasks.db_path = "test.db"
    delete_task = sql.Tasks.delete_task(1)
    assert delete_task == "Запись удалена"


time.sleep(5)


def test_db_delete():
    os.remove("./test.db")

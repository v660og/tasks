import sys
import sql
import db
import os.path
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QTableWidgetItem
from mainwindow import Ui_Form


class MainWindow(QtWidgets.QMainWindow, Ui_Form):
    """Класс описывает создание интерфейса

    Args:
        QtWidgets (PyQt6): виджеты
        Ui_Form (PyQt6): формы
    """

    def __init__(self, *args, obj=None, **kwargs):
        """Инициализатор"""
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.create_task)
        self.pushButton_2.clicked.connect(self.search_tasks)
        self.pushButton_3.clicked.connect(self.delete_task)
        self.pushButton_4.clicked.connect(self.update_task)

    def create_task(self) -> QtWidgets:
        """Создание задачи"""
        t_name: str = self.lineEdit.text()
        t_description: str = self.lineEdit_2.text()
        t_priority: str = self.lineEdit_3.text()
        t_deadline: str = self.lineEdit_4.text()

        if len(t_description) == 0:
            t_description = "NULL"
        else:
            t_description = t_description

        if len(t_priority) == 0:
            t_priority = 1

        if len(t_name) != 0:
            status = sql.Tasks.create_task(
                t_name, t_priority, t_description, t_deadline
            )
            self.label_6.setText(status)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()

        else:
            self.label_6.setText("Имя задачи не должно быть пустым!")

    def search_tasks(self) -> QtWidgets:
        """Поиск задач"""
        search_string: str = self.lineEdit_5.text()
        task_key: str = self.comboBox_2.currentText()
        if task_key == "По всем":
            tasks: list = sql.Tasks.search_task(search_string)
        else:
            tasks: list = sql.Tasks.search_task(search_string, task_key)

        rows: int = len(tasks)

        table = self.tableWidget
        table.setRowCount(rows)
        table.setSortingEnabled(True)

        row: int = 0
        for task in tasks:

            id_item = QTableWidgetItem()
            data = int(QTableWidgetItem(str(task[0])).text())
            id_item.setData(QtCore.Qt.ItemDataRole.DisplayRole, data)

            table.setItem(row, 0, QTableWidgetItem(id_item))
            table.setItem(row, 1, QTableWidgetItem(str(task[1])))
            table.setItem(row, 2, QTableWidgetItem(str(task[2])))
            table.setItem(row, 3, QTableWidgetItem(str(task[3])))
            table.setItem(row, 4, QTableWidgetItem(str(task[4])))
            table.setItem(row, 5, QTableWidgetItem(str(task[5])))
            table.setItem(row, 6, QTableWidgetItem(str(task[6])))

            row += 1

    def delete_task(self) -> QtWidgets:
        """Удаление задачи"""
        index_to_delete: str = self.lineEdit_6.text()
        self.label_6.setText(sql.Tasks.delete_task(index_to_delete))
        self.lineEdit_6.clear()

    def update_task(self) -> QtWidgets:
        """Обновление задачи"""
        index_to_update: str = self.lineEdit_7.text()
        new_value: str = self.lineEdit_8.text()
        task_key: str = self.comboBox.currentText()

        self.label_6.setText(
            sql.Tasks.update_task(index_to_update, task_key, new_value)
        )
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()


if __name__ == "__main__":

    if not os.path.exists("./tasks.db"):
        db.create_table()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()

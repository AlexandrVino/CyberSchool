from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
import sys
import sqlite3

class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../../static/ui/search_table.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('../../static/database/db.db')

    def fill_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT *"
                             f"FROM certificates").fetchall()
        self.table.setRowCount(len(self.result))
        self.table.setColumnCount(len(self.result[0]))

        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def find_in_table(self):
        pass

sys.__excepthook__ = sys.__excepthook__


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableWindow()
    window.show()
    sys.exit(app.exec())
    sys.excepthook = exception_hook
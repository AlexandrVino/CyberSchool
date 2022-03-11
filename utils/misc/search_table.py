from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import QtGui
import sys
import sqlite3

class EmptyLineEdit(Exception):
    pass


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../../static/ui/search_table.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('../../static/database/db.db')
        self.fill_table()
        self.initUi()

    def initUi(self):
        self.find_btn.clicked.connect(self.find_in_table)

    def fill_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT *"
                             f"FROM certificates").fetchall()
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        headers = ['№ п/п', '№ сертификата', 'наименование продукции', 'тип изделия', '№ заказа',
                  'организация', 'потребитель', 'ФИО выдавшего сертификат']
        for i, elem in enumerate(headers):
            header = QTableWidgetItem(elem)
            self.table.setHorizontalHeaderItem(i, header)
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.horizontalHeader().setStretchLastSection(True)

    def find_in_table(self):
        print(1)
        try:
            request = self.search_line.text()
            if not request:
                raise EmptyLineEdit

        except:
            print(f'Поисковая строка пуста')

        search_filter = self.search_criteria.currentText()





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
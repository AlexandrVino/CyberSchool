from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui
import sys
import sqlite3


class EmptyLineEdit(Exception):
    pass


class EmptyResult(Exception):
    pass


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('../../static/ui/search_table.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('../../static/database/db.db')
        self.columns_name = ['serial_number', 'number_certificate', 'product_name', 'product_type', 'order_number',
                             'consumer_organization', 'shop_manufacturer', 'full_name_of_the_certificate_issuer']
        self.reset_table()
        self.initUi()

    def initUi(self):
        self.find_btn.clicked.connect(self.find_in_table)
        self.reset_search_btn.clicked.connect(self.reset_table)

    def fill_table(self, result):
        try:
            if not result:
                raise EmptyResult
        except EmptyResult:
            self.error_message(f'Ничего не найдено')
            return
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        headers_name = ['№ п/п', '№ сертификата', 'наименование продукции', 'тип изделия', '№ заказа',
                  'организация', 'потребитель', 'ФИО выдавшего сертификат']
        # Создали заголовки к колонкам
        for i, elem in enumerate(headers_name):
            header = QTableWidgetItem(elem)
            self.table.setHorizontalHeaderItem(i, header)
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.horizontalHeader().setStretchLastSection(True)

    def reset_table(self): # Возвращение таблицы к первоначальному состоянию
        cur = self.con.cursor()
        self.fill_table(cur.execute(f"SELECT certificates.serial_number, "
                                    f"certificates.number_certificate, "
                                    f"certificates.product_name, "
                                    f"certificates.product_type, "
                                    f"certificates.order_number, "
                                    f"certificates.consumer_organization, "
                                    f"certificates.shop_manufacturer, "
                                    f"certificates.full_name_of_the_certificate_issuer FROM certificates").fetchall())
        self.search_line.setText("")

    def find_in_table(self):
        cur = self.con.cursor()
        try:
            request = self.search_line.text()
            if not request:
                raise EmptyLineEdit
        except:
            self.error_message(f'Поисковая строка пуста')
            return

        search_filter = self.search_criteria.currentIndex()
        if search_filter < 2:
            result = cur.execute(f"SELECT certificates.serial_number, "
                                 f"certificates.number_certificate, "
                                 f"certificates.product_name, "
                                 f"certificates.product_type, "
                                 f"certificates.order_number, "
                                 f"certificates.consumer_organization, "
                                 f"certificates.shop_manufacturer, "
                                 f"certificates.full_name_of_the_certificate_issuer "
                                 f"FROM certificates"
                                 f" WHERE {self.columns_name[search_filter]}={int(request)}").fetchall()
        else:
            result = cur.execute(f"SELECT certificates.serial_number, "
                                 f"certificates.number_certificate, "
                                 f"certificates.product_name, "
                                 f"certificates.product_type, "
                                 f"certificates.order_number, "
                                 f"certificates.consumer_organization, "
                                 f"certificates.shop_manufacturer, "
                                 f"certificates.full_name_of_the_certificate_issuer "
                                 f"FROM certificates"
                                 f" WHERE {self.columns_name[search_filter]} LIKE '%{request}%'").fetchall()

        self.fill_table(result)


    def error_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()


if __name__ == '__main__':
    sys.__excepthook__ = sys.__excepthook__


    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    app = QApplication(sys.argv)
    window = TableWindow()
    window.show()
    sys.exit(app.exec())
    sys.excepthook = exception_hook
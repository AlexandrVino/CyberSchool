import os
import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QAbstractItemView

from .certificate_window import *
from utils.misc.pdf_func import *


class EmptyLineEdit(Exception):
    pass


class EmptyResult(Exception):
    pass


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        uic.loadUi('static/ui/search_table.ui', self)  # Загружаем дизайн
        self.db = db
        self.columns_name = ['index_number', 'number_certificate', 'product_name', 'product_type', 'order_number',
                             'consumer_organization', 'shop_manufacturer', 'full_name_of_the_certificate_issuer']
        self.reset_table()
        self.initUi()

    def initUi(self):
        self.find_btn.clicked.connect(self.find_in_table)
        self.reset_search_btn.clicked.connect(self.reset_table)
        self.add_certificate_btn.clicked.connect(self.add_certificate)
        self.print_btn.clicked.connect(self.print_certificate)

    def fill_table(self, result):
        try:
            if not result:
                raise EmptyResult
        except EmptyResult:
            # self.error_message(f'Ничего не найдено')
            return
        self.table.setRowCount(len(result))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(len(result[0]))
        headers_name = ['№ п/п', '№ сертификата', 'наименование продукции', 'тип изделия', '№ заказа',
                        'организация', 'потребитель', 'ФИО выдавшего сертификат']
        # Создали заголовки к колонкам
        for i, elem in enumerate(headers_name):
            header = QTableWidgetItem(elem)
            header.setBackground(QtGui.QColor('#2c325c'))
            self.table.setHorizontalHeaderItem(i, header)
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.horizontalHeader().setStretchLastSection(True)

    def reset_table(self):  # Возвращение таблицы к первоначальному состоянию
        cur = self.db.con.cursor()
        self.fill_table(cur.execute(f"SELECT certificates.index_number, "
                                    f"certificates.number_certificate, "
                                    f"certificates.product_name, "
                                    f"certificates.product_type, "
                                    f"certificates.order_number, "
                                    f"certificates.consumer_organization, "
                                    f"certificates.shop_manufacturer, "
                                    f"certificates.full_name_of_the_certificate_issuer FROM certificates").fetchall())
        self.search_line.setText("")

    def find_in_table(self):
        cur = self.db.con.cursor()
        try:
            request = self.search_line.text()
            if not request:
                raise EmptyLineEdit
        except:
            self.error_message(f'Поисковая строка пуста')
            return

        search_filter = self.search_criteria.currentIndex()
        if search_filter < 1:
            result = cur.execute(f"SELECT certificates.index_number, "
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
            result = cur.execute(f"SELECT certificates.index_number, "
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

    def add_certificate(self):
        CertificateWindow(self, self.db).show()

    def print_btn(self):
        pass

    def print_certificate(self):
        current_cp = self.table.currentRow()
        if current_cp != -1:
            pass
            # запрос данных из бд
            data = self.db.get_certificate_for_pdf(
                self.table.item(current_cp, 0).text(), self.table.item(current_cp, 1).text())
            print(data)
            create_word(data)

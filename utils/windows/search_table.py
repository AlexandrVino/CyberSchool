import datetime
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
        self.setWindowTitle('Поиск сертификата')
        self.setWindowIcon(QIcon('static/ui/icon.ico'))
        self.find_btn.clicked.connect(self.find_in_table)
        self.reset_search_btn.clicked.connect(self.reset_table)
        self.add_certificate_btn.clicked.connect(self.add_certificate)
        self.print_btn.clicked.connect(self.print_certificate)
        self.table.cellClicked.connect(self.select_row)

    @staticmethod
    def add_changes_in_table(widget, json_data):
        print(json_data)

        if any(json_data):
            result = [
                json_data['index_number'],
                json_data['number_certificate'],
                json_data['product_name'],
                json_data['product_type'],
                json_data['order_number'],
                json_data['consumer_organization'],
                json_data['shop_manufacturer'],
                json_data['full_name_of_the_certificate_issuer']
            ]
            widget.insertRow(0)
            for i, arg in enumerate(result):
                widget.setItem(0, i, QTableWidgetItem(str(arg)))

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
        result.reverse()
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

    def select_row(self):
        self.table.clearSelection()
        row = self.table.currentRow()
        self.table.selectRow(row)

    def print_certificate(self):
        current_cp = self.table.currentRow()
        if current_cp != -1:
            pass
            # запрос данных из бд
            data = self.db.get_certificate_for_pdf(
                self.table.item(current_cp, 0).text(), self.table.item(current_cp, 1).text())
            if not any(data):
                return
            data = data[0]

            json_data = {
                "index_number": data[1],
                "number_certificate": data[2],
                "product_name": data[3],
                "product_number": data[4],
                "product_type": data[5],
                "order_number": data[6],
                "consumer_organization": data[7],
                "shop_manufacturer": data[8],
                "full_name_of_the_certificate_issuer": data[9],
                "kit": data[10],
                "draft_number": data[11],
                "release_date": datetime.now().strftime("%m/%d/%Y"),
                "technical_conditions": data[13]
            }
            create_word(json_data)

import os
import sqlite3
import sys
from datetime import datetime

from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox

from .error import Error


class CertificateWindow(QDialog):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.initUi()
        self.db = db

    def initUi(self):
        uic.loadUi('static/ui/certificate.ui', self)
        self.connect_buttons()
        self.active = 0
        self.line_edits = [
            self.index_number, self.number_certificate, self.product_name, self.kit, self.draft_number,
            self.production_number, self.product_type, self.order_number, self.consumer_organization,
            self.shop_manufacturer, self.full_name_of_the_certificate_issuer, self.technical_conditions
        ]
        self.line_edits[self.active].setFocus()

    def connect_buttons(self):
        self.save_btn.clicked.connect(self.save_changes)
        self.cancel_btn.clicked.connect(self.cancel_window)

    def keyPressEvent(self, event):

        if int(event.modifiers()) == Qt.ShiftModifier:
            if event.key() + 1 == Qt.Key_Enter:
                self.active -= 1
                if self.active < 0:
                    self.active = len(self.line_edits) - 1

        elif event.key() + 1 == Qt.Key_Enter:
            self.active += 1
            if self.active == len(self.line_edits):
                self.active = 0

        self.line_edits[self.active].setFocus()
        event.accept()

    def save_changes(self):
        Error('Пожалуйста проверьте данные\nперед сохранением!', self, 'accept').show()

    def cancel_window(self):
        self.destroy()

    def save_after_accept(self):
        json_data = {
            "serial_number": self.index_number.text(),
            "number_certificate": self.number_certificate.text(),
            "product_name": self.product_name.text(),
            "product_number": self.index_number.text(),
            "product_type": self.order_number.text(),
            "order_number": self.order_number.text(),
            "consumer_organization": self.consumer_organization.text(),
            "shop_manufacturer": self.shop_manufacturer.text(),
            "full_name_of_the_certificate_issuer": self.full_name_of_the_certificate_issuer.text(),
            "kit": self.kit.text(),
            "draft_number": self.draft_number.text(),
            "release_date": datetime.now().strftime("%m/%d/%Y"),
            "technical_conditions": self.technical_conditions.text()
        }

        if not all(value != '' for value in json_data.values()):
            Error('Пожалуйста заполните данные\nкорректно!', self).show()
            return

        if not json_data['serial_number'].isnumeric() or len(json_data['serial_number']) != 3:
            Error('Номер сертификата должен\nбыть числом! (XXX)', self).show()
            return

        lens = [2, 4]
        if not all(x.isnumeric() and len(x) == lens[i] for i, x in enumerate(json_data['number_certificate'].split('-'))) \
                or len(json_data['number_certificate'].split('-')) != 2:
            Error('Номер сертификата должен\nбыть в формате: XX-XXXX!', self).show()
            return

        self.db.add_certificate(json_data)
        self.destroy()

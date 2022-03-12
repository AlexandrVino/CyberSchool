import sqlite3
import sys
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox


class CertificateWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.active = 0
        self.line_edits = [
            self.index_number, self.number_certificate, self.product_name, self.kit, self.draft_number,
            self.order_number, self.product_type, self.release_date, self.consumer_organization, self.shop_manufacturer,
            self.full_name_of_the_certificate_issuer, self.technical_conditions
        ]
        self.line_edits[self.active].setFocus()

    def initUi(self):
        uic.loadUi('../../static/ui/certificate.ui', self)
        self.connect_buttons()

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
        json_data = {
            "serial_number": self.index_number.text(),
            "number_certificate": self.number_certificate.text(),
            "product_name": self.product_name.text(),
            "product_number": self.index_number.text(),
            "product_type": self.order_number.text(),
            "order_number": "self.order_number.text()",
            "consumer_organization": self.consumer_organization.text(),
            "shop_manufacturer": self.shop_manufacturer.text(),
            "full_name_of_the_certificate_issuer": self.full_name_of_the_certificate_issuer.text(),
            "kit": self.kit.text(),
            "draft_number": self.draft_number.text(),
            "release_date": self.release_date.text(),
            "technical_conditions": self.technical_conditions.text()
        }

    def cancel_window(self):
        self.destroy()


if __name__ == '__main__':
    sys.__excepthook__ = sys.__excepthook__


    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)


    app = QApplication(sys.argv)
    window = CertificateWindow()
    window.show()
    sys.exit(app.exec())
    sys.excepthook = exception_hook

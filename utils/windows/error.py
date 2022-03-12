from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class Error(QDialog):
    """
    Класс формы подтверждения/ошибки
    """

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.connect_ui()
        self.label.setText(text)
        self.parent = parent

    def connect_ui(self):
        """
        Метод подключения интерфейса
        :return:
        """

        name_ui = 'static/ui/error.ui'
        uic.loadUi(name_ui, self)
        for btn in self.buttonBox.buttons():
            if btn.text() == 'OK':
                btn.clicked.connect(self.save_finish)
                break

    def save_finish(self):
        self.parent.save_after_accept()
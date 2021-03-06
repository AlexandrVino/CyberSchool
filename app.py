import sys

from PyQt5.QtWidgets import QStyleFactory

from utils.misc.my_logging import *
from utils.db_api.db_functions import *
from utils.windows.search_table import *
from utils.windows.certificate_window import *


if __name__ == '__main__':
    db = DataBase('static/database/db.db')
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow(db)
    window.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec())

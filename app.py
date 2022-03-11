import sys

from utils.misc.my_logging import *


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())
    sys.excepthook = exception_hook

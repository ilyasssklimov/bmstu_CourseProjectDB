from PyQt5 import QtWidgets
import sys
from src.admin_panel.mainwindow import MainWindow
from src.logger.logger import init_logger
from src.logger.config import TargetType


def main():
    sys.path.append('.')
    init_logger(TargetType.ADMIN)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

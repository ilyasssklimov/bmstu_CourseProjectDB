from PyQt5 import QtWidgets
import sys
from src.admin_panel.mainwindow import MainWindow


def main():
    sys.path.append('.')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

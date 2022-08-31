from PyQt5 import QtWidgets
import sys
sys.path.append('.')

from src.admin_panel.mainwindow import MainWindow
from src.database.config import DB_DEFAULT_PARAMS
from src.database.pg_database import PgDatabase
from src.logger.logger import init_logger
from src.logger.config import TargetType


def main():
    init_logger(TargetType.ADMIN)
    database = PgDatabase(DB_DEFAULT_PARAMS)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(database)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

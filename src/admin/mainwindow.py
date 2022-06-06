import copy
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox

from src.admin.design import Ui_MainWindow
from src.controller.admin import AdminController
from src.database.config import DB_PARAMS
from src.database.database import PostgresDB
from src.model.tenant import Tenant


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.viewTable = None
        self.data = []
        self.upd_data = []

        db = PostgresDB(DB_PARAMS)
        self.controller = AdminController(db)

        self.table.itemChanged.connect(self.change_item)
        self.tenantGetBtn.clicked.connect(self.get_tenants)
        self.tenantSavBtn.clicked.connect(self.save_tenant_changes)
        self.addBtn.clicked.connect(self.add_row)
        self.delBtn.clicked.connect(self.del_row)

    def change_item(self, item):
        self.upd_data[item.row()][item.column()] = item.text()

    def add_row(self):
        self.table.setRowCount(self.table.rowCount() + 1)
        if self.viewTable == 1:
            self.upd_data.append(Tenant())

    def del_row(self):
        row = self.table.currentRow()
        if row == -1:
            return
        ans = QMessageBox.question(self, 'Удаление строки', f'Вы уверены, что хотите удалить строку с индексом {row}?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            del_tenant = self.controller.delete_tenant(self.data[row].id)
            if del_tenant:
                self.data.pop(row)
                self.upd_data.pop(row)
                self.table.removeRow(row)
                QMessageBox.about(self, 'Успех', f'Вы успешно удалили строку с индексом {row}')
            else:
                QMessageBox.about(self, 'Ошибка', f'Невозможно удалить строку с индексом = {row}')

    def save_tenant_changes(self):
        for tenant, tenant_upd in zip(self.data, self.upd_data):
            try:
                tenant_upd.set_id(int(tenant_upd.id))
                tenant_upd.set_age(int(tenant_upd.age))
                if tenant_upd.solvency == 'None':
                    tenant_upd.set_solvency('null')
            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с целочисленными значениями не могут быть другого типа')
            else:
                if tenant != tenant_upd:
                    if tenant.id != tenant_upd.id:
                        QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({tenant.id} != {tenant_upd.id})')
                    else:
                        get_tenant = self.controller.update_tenant(tenant_upd)
                        if not get_tenant:
                            QMessageBox.about(self, 'Ошибка', f'Невозможно обновить арендатора с id = {tenant_upd.id}')
                        else:
                            QMessageBox.about(self, 'Успех', f'Арендодатель с id = {tenant_upd.id} успешно обновлен')
                            self.data[self.data.index(tenant)] = tenant_upd

        for i in range(len(self.data), len(self.upd_data)):
            try:
                self.upd_data[i].set_id(int(self.upd_data[i].id))
                self.upd_data[i].set_age(int(self.upd_data[i].age))
                if self.upd_data[i].solvency == 'None':
                    self.upd_data[i].set_solvency('null')
            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с целочисленными значениями не могут быть другого типа')
            else:
                get_tenant = self.controller.add_tenant(self.upd_data[i])
                if not get_tenant:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить арендатора с id = {self.upd_data[i].id}')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {self.upd_data[i].id} успешно добавлен')
                    self.data.append(self.upd_data[i])

    def get_tenants(self):
        self.data = []
        self.upd_data = []
        self.viewTable = 1

        headers, tenants = self.controller.get_tenants()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(tenants))
        for row, tenant in enumerate(tenants):
            self.data.append(copy.deepcopy(tenant))
            self.upd_data.append(copy.deepcopy(tenant))
            for column in range(len(tenant)):
                self.table.setItem(row, column,  QTableWidgetItem(str(tenant[column])))

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

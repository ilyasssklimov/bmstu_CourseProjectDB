import copy
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox

from src.admin.design import Ui_MainWindow
from src.bot.states import EntityTypes
from src.controller.admin import AdminController
from src.database.config import DB_PARAMS
from src.database.database import PostgresDB
from src.model.tenant import Tenant
from src.model.landlord import Landlord


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.viewTable = None
        self.data = []
        self.upd_data = []

        db = PostgresDB(DB_PARAMS)
        self.controller = AdminController(db)

        self.get_funcs = {
            EntityTypes.TENANT: self.controller.get_tenants,
            EntityTypes.LANDLORD: self.controller.get_landlords
        }
        self.del_funcs = {
            EntityTypes.TENANT: self.controller.delete_tenant,
            EntityTypes.LANDLORD: self.controller.delete_landlord
        }

        self.table.itemChanged.connect(self.change_item)

        self.tenantGetBtn.clicked.connect(lambda: self.get_entities(EntityTypes.TENANT))
        self.tenantAddBtn.clicked.connect(lambda: self.add_row(EntityTypes.TENANT))
        self.tenantDelBtn.clicked.connect(lambda: self.delete_row(EntityTypes.TENANT))
        self.tenantSavBtn.clicked.connect(self.save_tenant_changes)

        self.landlordGetBtn.clicked.connect(lambda: self.get_entities(EntityTypes.LANDLORD))
        self.landlordAddBtn.clicked.connect(lambda: self.add_row(EntityTypes.LANDLORD))
        self.landlordDelBtn.clicked.connect(lambda: self.delete_row(EntityTypes.LANDLORD))
        self.landlordSavBtn.clicked.connect(self.save_landlord_changes)

    def change_item(self, item):
        self.upd_data[item.row()][item.column()] = item.text()

    def get_entities(self, entity_type: EntityTypes):
        self.data = []
        self.upd_data = []
        self.viewTable = entity_type

        headers, entities = self.get_funcs[entity_type]()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(entities))
        for row, entity in enumerate(entities):
            self.data.append(copy.deepcopy(entity))
            self.upd_data.append(copy.deepcopy(entity))
            for column in range(len(entity)):
                self.table.setItem(row, column,  QTableWidgetItem(str(entity[column])))

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

    def add_row(self, entity_type: EntityTypes):
        if entity_type != self.viewTable:
            return

        self.table.setRowCount(self.table.rowCount() + 1)
        if self.viewTable == EntityTypes.TENANT:
            self.upd_data.append(Tenant())
        elif self.viewTable == EntityTypes.LANDLORD:
            self.upd_data.append(Landlord())

    def delete_row(self, entity_type: EntityTypes):
        if entity_type != self.viewTable:
            return

        row = self.table.currentRow()
        if self.viewTable != entity_type or row == -1:
            return
        ans = QMessageBox.question(self, 'Удаление строки',
                                   f'Вы уверены, что хотите удалить строку с индексом {row + 1}?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            try:
                if self.del_funcs[entity_type](self.data[row].id):
                    self.table.removeRow(row)
                    self.data.pop(row)
                    self.upd_data.pop(row)
                    QMessageBox.about(self, 'Успех', f'Вы успешно удалили строку с индексом {row + 1}')
                else:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно удалить строку с индексом = {row + 1}')
            except IndexError:
                logging.info(f'There is no row with index {row} in DB')
                self.table.removeRow(row)
                self.upd_data.pop(row)

    def save_tenant_changes(self):
        if self.viewTable != EntityTypes.TENANT:
            return

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
                            self.data[self.data.index(tenant)] = copy.deepcopy(tenant_upd)

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
                    QMessageBox.about(self, 'Успех', f'Арендатор с id = {self.upd_data[i].id} успешно добавлен')
                    self.data.append(self.upd_data[i])

    def save_landlord_changes(self):
        if self.viewTable != EntityTypes.LANDLORD:
            return

        for landlord, landlord_upd in zip(self.data, self.upd_data):
            try:
                landlord_upd.set_id(int(landlord_upd.id))
                landlord_upd.set_age(int(landlord_upd.age))
                landlord_upd.set_rating(float(landlord_upd.rating))
            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с численными значениями не могут быть другого типа')
            else:
                if landlord != landlord_upd:
                    if landlord.id != landlord_upd.id:
                        QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({landlord.id} != {landlord_upd.id})')
                    else:
                        get_landlord = self.controller.update_landlord(landlord_upd)
                        if not get_landlord:
                            QMessageBox.about(self, 'Ошибка', f'Невозможно обновить арендодателя с id = {landlord_upd.id}')
                        else:
                            QMessageBox.about(self, 'Успех', f'Арендодатель с id = {landlord_upd.id} успешно обновлен')
                            self.data[self.data.index(landlord)] = copy.deepcopy(landlord_upd)

        for i in range(len(self.data), len(self.upd_data)):
            try:
                self.upd_data[i].set_id(int(self.upd_data[i].id))
                self.upd_data[i].set_age(int(self.upd_data[i].age))
            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с целочисленными значениями не могут быть другого типа')
            else:
                get_landlord = self.controller.add_landlord(self.upd_data[i])
                if not get_landlord:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить арендодателя с id = {self.upd_data[i].id}')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {self.upd_data[i].id} успешно добавлен')
                    self.data.append(self.upd_data[i])

import copy
import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox
from src.admin_panel.design import Ui_MainWindow
from src.bot.config import EntityType as EType
from src.controller.admin import AdminController
from src.database.config import DB_ADMIN_PARAMS
from src.database.database import PostgresDB
from src.generate_data.config import MOSCOW_FLATS_URL
from src.generate_data.flat import ParseFlats
from src.generate_data.user import GenerateData
from src.model.tenant import Tenant
from src.model.landlord import Landlord
from src.model.flat import Flat


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cur_table: EType = EType.NO_TYPE
        self.data: list[Tenant | Landlord | Flat] = []
        self.upd_data: list[Tenant | Landlord | Flat] = []

        self.__db = PostgresDB(DB_ADMIN_PARAMS)
        self.controller = AdminController(self.__db)

        self.get_funcs = {
            EType.TENANT: self.controller.get_tenants,
            EType.LANDLORD: self.controller.get_landlords,
            EType.FLAT: self.controller.get_flats
        }
        self.del_funcs = {
            EType.TENANT: self.controller.delete_tenant,
            EType.LANDLORD: self.controller.delete_landlord
        }

        self.table.itemChanged.connect(self.change_item)
        self.addBtn.clicked.connect(self.add_row)
        self.delBtn.clicked.connect(self.delete_row)

        self.tenantGetBtn.clicked.connect(lambda: self.get_entities(EType.TENANT))
        self.tenantSavBtn.clicked.connect(self.save_tenant_changes)

        self.landlordGetBtn.clicked.connect(lambda: self.get_entities(EType.LANDLORD))
        self.landlordSavBtn.clicked.connect(self.save_landlord_changes)

        self.flatGetBtn.clicked.connect(lambda: self.get_entities(EType.FLAT))

        self.tenantGenBtn.clicked.connect(lambda: self.generate_data(EType.TENANT))
        self.landlordGenBtn.clicked.connect(lambda: self.generate_data(EType.LANDLORD))
        self.flatGenBtn.clicked.connect(lambda: self.generate_data(EType.FLAT))

    def __del__(self):
        del self.__db

    def change_item(self, item):
        self.upd_data[item.row()][item.column()] = item.text()

    def get_entities(self, entity_type: EType):
        self.data = []
        self.upd_data = []
        self.cur_table = entity_type

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

    def add_row(self):
        if not self.cur_table:
            return

        self.table.setRowCount(self.table.rowCount() + 1)
        if self.cur_table == EType.TENANT:
            self.upd_data.append(Tenant())
        elif self.cur_table == EType.LANDLORD:
            self.upd_data.append(Landlord())

    def delete_row(self, entity_type: EType):
        row = self.table.currentRow()
        if not self.cur_table or row == -1:
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

    def generate_data(self, entity_type: EType):
        if entity_type == EType.TENANT or entity_type == EType.LANDLORD:
            try:
                n = int(self.tenantLinEdit.text()) if entity_type == EType.TENANT else int(self.landlordLinEdit.text())
                assert n > 0
            except (ValueError, AssertionError):
                QMessageBox.about(self, 'Ошибка', 'Количество пользователей должно быть положительным целым числом')
            else:
                generate = GenerateData(self.__db)
                generate.generate_users(entity_type, n)
                QMessageBox.about(self, 'Успех', f'Вы успешно сгенерировали {n} пользователей')
        elif entity_type == EType.FLAT:
            try:
                n = int(self.flatLinEdit.text())
                assert n > 0
            except (ValueError, AssertionError):
                QMessageBox.about(self, 'Ошибка', 'Количество квартир должно быть целым положительным числом')
            else:
                parse = ParseFlats(self.__db)
                parse.add_flats(MOSCOW_FLATS_URL, n)
                del parse
                QMessageBox.about(self, 'Успех', f'Вы успешно спарсили {n} квартир')

    def save_tenant_changes(self):
        if self.cur_table != EType.TENANT:
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
        if self.cur_table != EType.LANDLORD:
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

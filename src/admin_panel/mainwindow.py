import copy
import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox
from src.admin_panel.design import Ui_MainWindow
from src.bot.config import EntityType as EType
from src.controller.admin import AdminController
from src.database.config import DB_DEFAULT_PARAMS, RolesDB
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
        self.cur_entity: EType = EType.NO_TYPE
        self.data: list[Tenant | Landlord | Flat] = []
        self.upd_data: list[Tenant | Landlord | Flat] = []

        self.__db = PostgresDB(DB_DEFAULT_PARAMS)
        self.__db.execute_init_files()
        self.__db.set_role(RolesDB.ADMIN)
        self.controller: AdminController = AdminController(self.__db)

        self.get_funcs = {
            EType.TENANT: self.controller.get_tenants,
            EType.LANDLORD: self.controller.get_landlords,
            EType.FLAT: self.controller.get_flats
        }
        self.del_funcs = {
            EType.TENANT: self.controller.delete_tenant,
            EType.LANDLORD: self.controller.delete_landlord,
            EType.FLAT: self.controller.delete_flat
        }

        self.table.itemChanged.connect(self.change_item)
        self.addBtn.clicked.connect(self.add_row)
        self.delBtn.clicked.connect(self.delete_row)

        self.tenantGetBtn.clicked.connect(lambda: self.get_entities(EType.TENANT))
        self.tenantSavBtn.clicked.connect(self.save_tenant_changes)

        self.landlordGetBtn.clicked.connect(lambda: self.get_entities(EType.LANDLORD))
        self.landlordSavBtn.clicked.connect(self.save_landlord_changes)

        self.flatGetBtn.clicked.connect(lambda: self.get_entities(EType.FLAT))
        self.flatSavBtn.clicked.connect(self.save_flat_changes)

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
        self.cur_entity = entity_type

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
        self.table.scrollToTop()

    def add_row(self):
        if not self.cur_entity:
            return

        self.table.setRowCount(self.table.rowCount() + 1)
        if self.cur_entity == EType.TENANT:
            self.upd_data.append(Tenant())
        elif self.cur_entity == EType.LANDLORD:
            self.upd_data.append(Landlord())
        elif self.cur_entity == EType.FLAT:
            self.upd_data.append(Flat())
        self.table.scrollToBottom()

    def delete_row(self):
        row = self.table.currentRow()
        if self.cur_entity == EType.NO_TYPE or row == -1:
            return

        ans = QMessageBox.question(self, 'Удаление строки',
                                   f'Вы уверены, что хотите удалить строку с индексом {row + 1}?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            try:
                if self.del_funcs[self.cur_entity](self.data[row].id):
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
        if entity_type == EType.NO_TYPE:
            return

        ans = QMessageBox.question(self, 'Генерация данных', f'Вы уверены, что хотите сгенерировать данные?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.No:
            return

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

        self.get_entities(entity_type)

    def save_tenant_changes(self):
        def adjust_tenant(adjusted_tenant: Tenant) -> bool:
            try:
                adjusted_tenant.set_id(int(adjusted_tenant.id))
                adjusted_tenant.set_age(int(adjusted_tenant.age))

                assert 14 <= adjusted_tenant.age <= 100
                assert adjusted_tenant.solvency.lower() in ('true', 'false', 'null', 'none')
                if adjusted_tenant.solvency.lower() == 'none':
                    adjusted_tenant.set_solvency('null')

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с целочисленными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Платежеспособность должна принимать значения true или false, '
                                                  'возраст должен принадлежать значениям [14, 100]')
            else:
                return True
            return False

        if self.cur_entity != EType.TENANT:
            return

        for tenant, tenant_upd in zip(self.data, self.upd_data):
            if not tenant_upd.id.isdigit() or tenant.id != int(tenant_upd.id):
                QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({tenant.id} != {tenant_upd.id})')
            elif adjust_tenant(tenant_upd) and tenant != tenant_upd:
                result_tenant = self.controller.update_tenant(tenant_upd)
                if not result_tenant:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно обновить арендатора с id = {tenant_upd.id}. '
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {tenant_upd.id} успешно обновлен')
                    self.data[self.data.index(tenant)] = copy.deepcopy(tenant_upd)

        for i in range(len(self.data), len(self.upd_data)):
            if adjust_tenant(self.upd_data[i]):
                result_tenant = self.controller.add_tenant(self.upd_data[i])
                if not result_tenant:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить арендатора с id = {self.upd_data[i].id}. '
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендатор с id = {self.upd_data[i].id} успешно добавлен')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.TENANT)

    def save_landlord_changes(self):
        def adjust_landlord(adjusted_landlord: Landlord) -> bool:
            try:
                adjusted_landlord.set_id(int(adjusted_landlord.id))
                adjusted_landlord.set_age(int(adjusted_landlord.age))
                adjusted_landlord.set_rating(float(adjusted_landlord.rating))

                assert 14 <= adjusted_landlord.age <= 100
                assert 0. <= adjusted_landlord.rating <= 10.

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с численными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Возраст должен принадлежать значениям [14, 100], '
                                                  'рейтинг - [0.0, 10.0]')
            else:
                return True
            return False

        if self.cur_entity != EType.LANDLORD:
            return

        for landlord, landlord_upd in zip(self.data, self.upd_data):
            if not landlord_upd.id.isdigit() or landlord.id != int(landlord_upd.id):
                QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({landlord.id} != {landlord_upd.id})')
            elif adjust_landlord(landlord_upd) and landlord != landlord_upd:
                result_landlord = self.controller.update_landlord(landlord_upd)
                if not result_landlord:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно обновить арендодателя с id = {landlord_upd.id}.'
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {landlord_upd.id} успешно обновлен')
                    self.data[self.data.index(landlord)] = copy.deepcopy(landlord_upd)

        for i in range(len(self.data), len(self.upd_data)):
            if adjust_landlord(self.upd_data[i]):
                result_landlord = self.controller.add_landlord(self.upd_data[i])
                if not result_landlord:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить арендодателя с id = {self.upd_data[i].id}. '
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {self.upd_data[i].id} успешно добавлен')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.LANDLORD)

    def save_flat_changes(self):
        def adjust_flat(adjusted_flat: Flat) -> bool:
            try:
                adjusted_flat.set_owner_id(int(adjusted_flat.owner_id))
                adjusted_flat.set_price(int(adjusted_flat.price))
                adjusted_flat.set_rooms(int(adjusted_flat.rooms))
                adjusted_flat.set_square(float(adjusted_flat.square))
                adjusted_flat.set_floor(int(adjusted_flat.floor))
                adjusted_flat.set_max_floor(int(adjusted_flat.max_floor))

                if not self.controller.check_landlord(adjusted_flat.owner_id):
                    raise IndexError
                assert adjusted_flat.price > 0 and adjusted_flat.rooms > 0 and adjusted_flat.square > 0

                assert adjusted_flat.floor > 0 and adjusted_flat.max_floor > 0
                if adjusted_flat.floor > adjusted_flat.max_floor:
                    raise AttributeError

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с численными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Поля "Цена", "Комнаты", "Площадь", "Этаж", "Максимальный этаж" '
                                                  'должны быть положительными числами')
            except IndexError:
                QMessageBox.about(self, 'Ошибка', f'Арендодателя с id {adjusted_flat.owner_id} не существует')
            except AttributeError:
                QMessageBox.about(self, 'Ошибка', 'Этаж не может быть больше максимального этажа')
            else:
                return True
            return False

        if self.cur_entity != EType.FLAT:
            return

        for flat, flat_upd in zip(self.data, self.upd_data):
            if not flat_upd.id.isdigit() or int(flat.id) != int(flat_upd.id):
                QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({flat.id} != {flat_upd.id})')
            elif adjust_flat(flat_upd) and flat != flat_upd:
                result_flat = self.controller.update_flat(flat_upd)
                if not result_flat:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно обновить квартиру с id = {flat_upd.id}.'
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Квартира с id = {flat_upd.id} успешно обновлена')
                    self.data[self.data.index(flat)] = copy.deepcopy(flat_upd)

        for i in range(len(self.data), len(self.upd_data)):
            if adjust_flat(self.upd_data[i]):
                result_flat = self.controller.add_flat(self.upd_data[i])
                if not result_flat:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить квартиру с id = {self.upd_data[i].id}. '
                                                      f'Проверьте введенные данные на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Квартира с id = {self.upd_data[i].id} успешно добавлена '
                                                     f'(примечание: id присвоен автоматически)')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.FLAT)

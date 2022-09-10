import copy
import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox
from src.admin_panel.design import Ui_MainWindow
from src.bot.config import EntityType as EType
from src.controller.admin import AdminController
from src.database.config import RolesDB
from src.database.database import BaseDatabase
from src.generate_data.config import MOSCOW_FLATS_URL
from src.generate_data.data import DataGenerator
from src.model.flat import Flat
from src.model.landlord import Landlord
from src.model.neighborhood import Neighborhood
from src.model.tenant import Tenant
from src.model.goods import Goods


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, database: BaseDatabase):
        super().__init__()
        self.setupUi(self)
        self.cur_entity: EType = EType.NO_TYPE
        self.data: list[Tenant | Landlord | Flat | Neighborhood | Goods] = []
        self.upd_data: list[Tenant | Landlord | Flat | Neighborhood | Goods] = []

        self.__db = database
        self.__db.set_role(RolesDB.ADMIN)
        self.controller: AdminController = AdminController(self.__db)
        self.gen_data: DataGenerator = DataGenerator(self.__db)

        self.get_funcs = {
            EType.TENANT: self.controller.get_tenants,
            EType.LANDLORD: self.controller.get_landlords,
            EType.FLAT: self.controller.get_flats,
            EType.NEIGHBORHOOD: self.controller.get_neighborhoods,
            EType.GOODS: self.controller.get_goods
        }
        self.del_funcs = {
            EType.TENANT: self.controller.delete_tenant,
            EType.LANDLORD: self.controller.delete_landlord,
            EType.FLAT: self.controller.delete_flat,
            EType.NEIGHBORHOOD: self.controller.delete_neighborhood,
            EType.GOODS: self.controller.delete_goods
        }
        self.clr_funcs = {
            EType.TENANT: self.controller.delete_tenants,
            EType.LANDLORD: self.controller.delete_landlords,
            EType.FLAT: self.controller.delete_flats,
            EType.NEIGHBORHOOD: self.controller.delete_neighborhoods,
            EType.GOODS: self.controller.delete_goods
        }
        self.sav_funcs = {
            EType.TENANT: self.__save_tenant_changes,
            EType.LANDLORD: self.__save_landlord_changes,
            EType.FLAT: self.__save_flat_changes,
            EType.NEIGHBORHOOD: self.__save_neighborhood_changes,
            EType.GOODS: self.__save_goods_changes
        }
        self.models = {
            EType.TENANT: Tenant(),
            EType.LANDLORD: Landlord(),
            EType.FLAT: Flat(),
            EType.NEIGHBORHOOD: Neighborhood(),
            EType.GOODS: Goods()
        }

        self.table.itemChanged.connect(self.change_item)
        self.addBtn.clicked.connect(self.add_row)
        self.delBtn.clicked.connect(self.delete_row)
        self.clrBtn.clicked.connect(self.clear_table)
        self.savBtn.clicked.connect(self.save_data)
        self.genBtn.clicked.connect(self.generate_data)

        self.getTenantBtn.clicked.connect(lambda: self.get_entities(EType.TENANT))
        self.getLandlordBtn.clicked.connect(lambda: self.get_entities(EType.LANDLORD))
        self.getFlatBtn.clicked.connect(lambda: self.get_entities(EType.FLAT))
        self.getNeighborBtn.clicked.connect(lambda: self.get_entities(EType.NEIGHBORHOOD))
        self.getGoodsBtn.clicked.connect(lambda: self.get_entities(EType.GOODS))

    def closeEvent(self, event):
        self.__db.disconnect_db()
        super().closeEvent(event)

    def change_item(self, item):
        self.upd_data[item.row()][self.table.horizontalHeaderItem(item.column()).text()] = item.text()

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
            for column, name in enumerate(entity.get_params()):
                self.table.setItem(row, column, QTableWidgetItem(str(name)))

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.scrollToTop()

    def add_row(self):
        if self.cur_entity == EType.NO_TYPE:
            return

        self.table.setRowCount(self.table.rowCount() + 1)
        self.upd_data.append(self.models[self.cur_entity])
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
                del_obj = self.del_funcs[self.cur_entity](self.data[row].id)
                if del_obj:
                    self.table.removeRow(row)
                    self.data.pop(row)
                    self.upd_data.pop(row)
                    QMessageBox.about(self, 'Успех', f'Вы успешно удалили объект с id = {del_obj.id}')
                else:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно удалить объект с id = {del_obj.id}')
            except IndexError:
                logging.info(f'There is no row with index {row} in DB')
                self.table.removeRow(row)
                self.upd_data.pop(row)

    def clear_table(self):
        if self.cur_entity == EType.NO_TYPE:
            return

        ans = QMessageBox.question(self, 'Удаление строки', 'Вы уверены, что хотите очистить таблицу?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            if self.clr_funcs[self.cur_entity]():
                self.get_entities(self.cur_entity)
                QMessageBox.about(self, 'Успех', 'Вы успешно очистили текущую таблицу')
            else:
                QMessageBox.about(self, 'Ошибка', 'Произошла ошибка во время удаления')

    def generate_data(self):
        if self.cur_entity == EType.NO_TYPE:
            return

        ans = QMessageBox.question(self, 'Генерация данных', f'Вы уверены, что хотите сгенерировать данные?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ans == QMessageBox.No:
            return

        try:
            n = int(self.lineEdit.text())
            assert n > 0
        except (ValueError, AssertionError):
            QMessageBox.about(self, 'Ошибка', 'Количество должно быть целым положительным числом')
            self.lineEdit.setText('100')
        else:
            if self.cur_entity == EType.TENANT or self.cur_entity == EType.LANDLORD:
                count = self.gen_data.generate_users(self.cur_entity, n)
                QMessageBox.about(self, 'Успех', f'Вы успешно сгенерировали {count} / {n} пользователей')

            elif self.cur_entity == EType.FLAT:
                count = self.gen_data.parse_flats(MOSCOW_FLATS_URL, n)
                QMessageBox.about(self, 'Успех', f'Вы успешно спарсили {count} / {n} квартир')

            elif self.cur_entity == EType.NEIGHBORHOOD:
                count = self.gen_data.generate_neighborhoods(n)
                QMessageBox.about(self, 'Успех', f'Вы успешно сгенерировали {count} / {n} объявлений о соседстве')

            elif self.cur_entity == EType.GOODS:
                count = self.gen_data.generate_goods(n)
                QMessageBox.about(self, 'Успех', f'Вы успешно сгенерировали {count} / {n} объявлений о товарах')

            self.get_entities(self.cur_entity)

    def save_data(self):
        if self.cur_entity == EType.NO_TYPE:
            return
        self.sav_funcs[self.cur_entity]()

    def __save_tenant_changes(self):
        def adjust_tenant(adjusted_tenant: Tenant) -> bool:
            try:
                adjusted_tenant.set_id(int(adjusted_tenant.id))
                adjusted_tenant.set_age(int(adjusted_tenant.age))

                assert 14 <= adjusted_tenant.age <= 100
                assert adjusted_tenant.sex in ('M', 'F')
                assert adjusted_tenant.solvency.lower() in ('true', 'false', 'null', 'none')
                if adjusted_tenant.solvency.lower() == 'none':
                    adjusted_tenant.set_solvency('null')

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с целочисленными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Платежеспособность должна принимать значения true, false или none; '
                                                  'пол - M или F; '
                                                  'возраст должен принадлежать значениям [14, 100]')
            else:
                return True

            return False

        if self.cur_entity != EType.TENANT:
            return

        for tenant, tenant_upd in zip(self.data, self.upd_data):
            if not str(tenant_upd.id).isdigit() or tenant.id != int(tenant_upd.id):
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
                    QMessageBox.about(self, 'Успех', f'Арендатор с id = {result_tenant.id} успешно добавлен')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.TENANT)

    def __save_landlord_changes(self):
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
            if not str(landlord_upd.id).isdigit() or landlord.id != int(landlord_upd.id):
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
                    QMessageBox.about(self, 'Успех', f'Арендодатель с id = {result_landlord.id} успешно добавлен')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.LANDLORD)

    def __save_flat_changes(self):
        def adjust_flat(adjusted_flat: Flat) -> bool:
            try:
                adjusted_flat.set_id(int(adjusted_flat.id))
                if adjusted_flat.owner_id.lower() != 'none':
                    adjusted_flat.set_owner_id(int(adjusted_flat.owner_id))
                else:
                    adjusted_flat.set_owner_id(None)
                adjusted_flat.set_price(int(adjusted_flat.price))
                adjusted_flat.set_rooms(int(adjusted_flat.rooms))
                adjusted_flat.set_square(float(adjusted_flat.square))
                adjusted_flat.set_floor(int(adjusted_flat.floor))
                adjusted_flat.set_max_floor(int(adjusted_flat.max_floor))

                if adjusted_flat.owner_id and not self.controller.check_landlord(adjusted_flat.owner_id):
                    raise IndexError
                assert adjusted_flat.price > 0 and adjusted_flat.rooms > 0 and adjusted_flat.square > 0

                assert adjusted_flat.floor >= 0 and adjusted_flat.max_floor >= 0
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
            if not str(flat_upd.id).isdigit() or flat.id != int(flat_upd.id):
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
                    QMessageBox.about(self, 'Успех', f'Квартира с id = {result_flat.id} успешно добавлена '
                                                     f'(примечание: id присвоен автоматически)')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.FLAT)

    def __save_neighborhood_changes(self):
        def adjust_neighborhood(adjusted_neighborhood: Neighborhood) -> bool:
            try:
                adjusted_neighborhood.set_id(int(adjusted_neighborhood.id))
                if adjusted_neighborhood.tenant_id.lower() != 'none':
                    adjusted_neighborhood.set_tenant_id(int(adjusted_neighborhood.tenant_id))
                else:
                    adjusted_neighborhood.set_tenant_id(None)
                adjusted_neighborhood.set_neighbors(int(adjusted_neighborhood.neighbors))
                adjusted_neighborhood.set_price(int(adjusted_neighborhood.price))

                if (adjusted_neighborhood.tenant_id and
                        not self.controller.check_tenant(adjusted_neighborhood.tenant_id)):
                    raise IndexError

                assert adjusted_neighborhood.neighbors > 0 and adjusted_neighborhood.price > 0
                assert adjusted_neighborhood.sex in ('M', 'F', 'N')

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с численными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Поля "Соседи", "Цена" должны быть положительными числами; '
                                                  'пол - M, F или N')
            except IndexError:
                QMessageBox.about(self, 'Ошибка', f'Арендатора с id {adjusted_neighborhood.tenant_id} не существует')
            else:
                return True

            return False

        if self.cur_entity != EType.NEIGHBORHOOD:
            return

        for neighborhood, neighborhood_upd in zip(self.data, self.upd_data):
            if not str(neighborhood_upd.id).isdigit() or int(neighborhood.id) != int(neighborhood_upd.id):
                QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({neighborhood.id} != {neighborhood_upd.id})')
            elif adjust_neighborhood(neighborhood_upd) and neighborhood != neighborhood_upd:
                result_neighborhood = self.controller.update_neighborhood(neighborhood_upd)
                if not result_neighborhood:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно обновить объявление о соседстве с id = '
                                                      f'{neighborhood_upd.id}. Проверьте введенные данные '
                                                      f'на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Объявление о соседстве с '
                                                     f'id = {neighborhood_upd.id} успешно обновлено')
                    self.data[self.data.index(neighborhood)] = copy.deepcopy(neighborhood_upd)

        for i in range(len(self.data), len(self.upd_data)):
            if adjust_neighborhood(self.upd_data[i]):
                result_neighborhood = self.controller.add_neighborhood(self.upd_data[i])
                if not result_neighborhood:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить объявление о соседстве с id = '
                                                      f'{self.upd_data[i].id}. Проверьте введенные данные '
                                                      f'на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Объявление о соседстве с id = {result_neighborhood.id} '
                                                     f'успешно добавлено (примечание: id присвоен автоматически)')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.NEIGHBORHOOD)

    def __save_goods_changes(self):
        def adjust_goods(adjusted_goods: Goods) -> bool:
            try:
                adjusted_goods.set_id(int(adjusted_goods.id))
                if adjusted_goods.owner_id.lower() != 'none':
                    adjusted_goods.set_owner_id(int(adjusted_goods.owner_id))
                else:
                    adjusted_goods.set_owner_id(None)
                adjusted_goods.set_price(int(adjusted_goods.price))

                assert adjusted_goods.bargain.lower() in ('true', 'false', 'null', 'none')
                if adjusted_goods.bargain.lower() == 'none':
                    adjusted_goods.set_bargain('null')

                assert adjusted_goods.condition in ('E', 'G', 'S', 'U', 'T')
                assert adjusted_goods.price > 0
                if adjusted_goods.owner_id and not self.controller.check_tenant(adjusted_goods.owner_id):
                    raise IndexError

            except ValueError:
                QMessageBox.about(self, 'Ошибка', 'Поля с численными значениями не могут быть другого типа')
            except AssertionError:
                QMessageBox.about(self, 'Ошибка', 'Торг должен принимать значения true, false или none; '
                                                  'состояние - E, G, S, U или T; '
                                                  'цена должна быть положительными числами)')
            except IndexError:
                QMessageBox.about(self, 'Ошибка', f'Арендатора с id {adjusted_goods.owner_id} не существует')
            else:
                return True

            return False

        if self.cur_entity != EType.GOODS:
            return

        for goods, goods_upd in zip(self.data, self.upd_data):
            if not str(goods_upd.id).isdigit() or int(goods.id) != int(goods_upd.id):
                QMessageBox.about(self, 'Ошибка', f'Нельзя изменять ID ({goods.id} != {goods_upd.id})')
            elif adjust_goods(goods_upd) and goods != goods_upd:
                result_goods = self.controller.update_goods(goods_upd)
                if not result_goods:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно обновить объявление о товаре с id = '
                                                      f'{goods_upd.id}. Проверьте введенные данные '
                                                      f'на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Объявление о товаре с id = {goods_upd.id} успешно обновлено')
                    self.data[self.data.index(goods)] = copy.deepcopy(goods_upd)

        for i in range(len(self.data), len(self.upd_data)):
            if adjust_goods(self.upd_data[i]):
                result_goods = self.controller.add_goods(self.upd_data[i])
                if not result_goods:
                    QMessageBox.about(self, 'Ошибка', f'Невозможно добавить объявление о товаре с id = '
                                                      f'{self.upd_data[i].id}. Проверьте введенные данные '
                                                      f'на корректность')
                else:
                    QMessageBox.about(self, 'Успех', f'Объявление о товаре с id = {result_goods.id} '
                                                     f'успешно добавлено (примечание: id присвоен автоматически)')
                    self.data.append(self.upd_data[i])

        self.get_entities(EType.GOODS)

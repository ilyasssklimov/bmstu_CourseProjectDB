import logging
import psycopg2 as ps
from src.database.database import PostgresDB
from src.model.flat import Flat
from src.model.landlord import Landlord
from src.model.tenant import Tenant


class AdminController:
    def __init__(self, db: PostgresDB):
        self.__db = db

    # tenant methods
    def get_tenants(self):
        headers = ['id', 'full_name', 'sex', 'city', 'personal_qualities', 'age', 'solvency']
        tenants = [Tenant(*tenant) for tenant in self.__db.get_tenants()]
        return headers, tenants

    def add_tenant(self, tenant: Tenant):
        try:
            add_tenant = Tenant(*self.__db.add_tenant(*tenant.get_params()))
            return add_tenant
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while adding tenant with name \'{tenant.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding tenant with name \'{tenant.full_name}\'')

        return Tenant()

    def update_tenant(self, tenant: Tenant):
        try:
            upd_tenant = Tenant(*self.__db.update_tenant(*tenant.get_params()))
            return upd_tenant
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while updating tenant with name \'{tenant.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating tenant with name \'{tenant.full_name}\'')

        return Tenant()

    def delete_tenant(self, tenant_id: int):
        try:
            del_tenant = Tenant(*self.__db.delete_tenant(tenant_id))
            return del_tenant
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting tenant with id = {tenant_id}')

        return Tenant()

    # landlord methods
    def get_landlords(self):
        headers = ['id', 'full_name', 'city', 'rating', 'age']
        landlords = [Landlord(*landlord) for landlord in self.__db.get_landlords()]
        return headers, landlords

    def delete_landlord(self, landlord_id: int):
        try:
            del_landlord = Tenant(*self.__db.delete_landlord(landlord_id))
            return del_landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting landlord with id = {landlord_id}')

        return Landlord()

    def add_landlord(self, landlord: Landlord):
        try:
            add_landlord = Landlord(*self.__db.add_landlord(*landlord.get_params()))
            return add_landlord
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while adding landlord with name \'{landlord.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding landlord with name \'{landlord.full_name}\'')

        return Landlord()

    def update_landlord(self, landlord: Landlord):
        try:
            upd_landlord = Landlord(*self.__db.update_landlord(*landlord.get_params()))
            return upd_landlord
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while updating landlord with name \'{landlord.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating landlord with name \'{landlord.full_name}\'')

        return Landlord()

    # flat methods
    def get_flats(self):
        headers = ['id', 'owner_id', 'price', 'rooms', 'square', 'address',
                   'metro', 'floor', 'max_floor', 'description']
        flats = [Flat(*flat) for flat in self.__db.get_flats()]
        return headers, flats

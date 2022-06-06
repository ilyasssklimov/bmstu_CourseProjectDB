import logging
import psycopg2 as ps

from src.database.database import PostgresDB
from src.model.tenant import Tenant


class AdminController:
    def __init__(self, db: PostgresDB):
        self.__db = db

    def get_tenants(self):
        headers = ['id', 'full_name', 'sex', 'city', 'personal_qualities', 'age', 'solvency']
        tenants = [Tenant(*tenant) for tenant in self.__db.get_tenants()]
        return headers, tenants

    def add_tenant(self, tenant):
        try:
            add_tenant = Tenant(*self.__db.add_tenant(tenant.id, tenant.full_name, tenant.sex, tenant.city,
                                                      tenant.qualities, tenant.age, tenant.solvency))
            return add_tenant
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while registration tenant with name \'{tenant.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding tenant with name \'{tenant.full_name}\'')

        return Tenant()

    def update_tenant(self, tenant):
        try:
            upd_tenant = Tenant(*self.__db.update_tenant(tenant.id, tenant.full_name, tenant.sex, tenant.city,
                                                         tenant.qualities, tenant.age, tenant.solvency))
            return upd_tenant
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while updating tenant with name \'{tenant.full_name}\'')
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating tenant with name \'{tenant.full_name}\'')

        return Tenant()

    def delete_tenant(self, tenant_id):
        try:
            del_tenant = Tenant(*self.__db.delete_tenant(tenant_id))
            return del_tenant
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting tenant with id = {tenant_id}')

        return Tenant()

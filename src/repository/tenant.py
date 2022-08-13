import logging
from src.database.database import BaseDatabase
from src.model.tenant import Tenant


class TenantRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def get_tenants(self) -> list[Tenant]:
        tenants = [Tenant(*tenant) for tenant in self.__db.get_tenants()]
        tenants.sort(key=lambda tenant: tenant.id)
        return tenants

    def add_tenant(self, tenant: Tenant) -> Tenant:
        try:
            new_tenant = Tenant(*self.__db.add_tenant(*tenant.get_params()))
            return new_tenant
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding tenant with name \'{tenant.full_name}\'')
        return Tenant()

    def update_tenant(self, tenant: Tenant) -> Tenant:
        try:
            upd_tenant = Tenant(*self.__db.update_tenant(*tenant.get_params()))
            return upd_tenant
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating tenant with name \'{tenant.full_name}\'')

        return Tenant()

    def delete_tenant(self, tenant_id: int) -> Tenant:
        try:
            del_tenant = Tenant(*self.__db.delete_tenant(tenant_id))
            return del_tenant
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting tenant with id = {tenant_id}')

        return Tenant()

from src.controller.guest import GuestController


class TenantController(GuestController):
    def check_tenant(self, tenant_id: int):
        return self._db.check_tenant(tenant_id)

    def check_landlord(self, landlord_id: int):
        return self._db.check_landlord(landlord_id)

    def register_tenant(self, *args):
        raise AttributeError('\'B\' object has no attribute \'register_tenant\'')

    def register_landlord(self, *args):
        raise AttributeError('\'B\' object has no attribute \'register_landlord\'')

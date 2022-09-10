from src.controller.guest import GuestController
from src.controller.tenant import TenantController
from src.model.flat import Flat
from src.model.tenant import Tenant


class LandlordController(GuestController):
    get_flats_filters = TenantController.get_flats_filters
    get_neighborhoods_filters = TenantController.get_neighborhoods_filters
    get_goods_filters = TenantController.get_goods_filters

    def add_flat(self, flat: Flat) -> Flat:
        new_flat = self._flat_repo.add_flat(flat)
        return new_flat

    def add_photo(self, flat_id: int, photo: str) -> str:
        photo = self._flat_repo.add_photo(flat_id, photo)
        return photo

    def get_tenants_subscription(self, landlord_id: int) -> list[Tenant]:
        tenants = self._landlord_repo.get_tenants_subscription(landlord_id)
        return tenants

    def get_subscribed_flat_tenants(self, price: int, rooms: int, square: float, metro: str) -> list[Tenant]:
        tenants = self._tenant_repo.get_subscribed_flat_tenants(price, rooms, square, metro)
        return tenants

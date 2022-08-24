from src.controller.guest import GuestController
from src.model.flat import Flat


class TenantController(GuestController):
    def check_tenant(self, tenant_id: int):
        return self._tenant_repo.check_tenant(tenant_id)

    def check_landlord(self, landlord_id: int):
        return self._landlord_repo.check_landlord(landlord_id)

    def get_flats_filters(self, price: tuple[int, int], rooms: tuple[int, int], square: tuple[float, float],
                          metro: list[str]) -> tuple[list[Flat], list[list[str]]]:
        flats = self._flat_repo.get_flats_filters(price, rooms, square, metro)
        photos = [self._flat_repo.get_photos(flat.id) for flat in flats]
        return flats, photos

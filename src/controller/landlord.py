from src.controller.tenant import TenantController
from src.model.flat import Flat


class LandlordController(TenantController):
    def add_flat(self, flat: Flat) -> Flat:
        new_flat = self._flat_repo.add_flat(flat)
        return new_flat

    def add_photo(self, flat_id: int, photo: str) -> str:
        photo = self._flat_repo.add_photo(flat_id, photo)
        return photo

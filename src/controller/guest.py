from multipledispatch import dispatch
from src.database.database import BaseDatabase
from src.model.flat import Flat
from src.model.tenant import Tenant
from src.model.landlord import Landlord
from src.repository.tenant import TenantRepository
from src.repository.landlord import LandlordRepository
from src.repository.flat import FlatRepository
from src.repository.neighborhood import NeighborhoodRepository
from src.repository.goods import GoodsRepository


class GuestController:
    def __init__(self, db: BaseDatabase):
        self._tenant_repo = TenantRepository(db)
        self._landlord_repo = LandlordRepository(db)
        self._flat_repo = FlatRepository(db)
        self._neighborhood_repo = NeighborhoodRepository(db)
        self._goods_repo = GoodsRepository(db)

    def check_tenant(self, tenant_id: int) -> bool:
        return self._tenant_repo.check_tenant(tenant_id)

    def register_tenant(self, tenant: Tenant) -> Tenant:
        tenant = self._tenant_repo.add_tenant(tenant)
        return tenant

    def check_landlord(self, landlord_id: int) -> bool:
        return self._landlord_repo.check_landlord(landlord_id)

    def register_landlord(self, landlord: Landlord) -> Landlord:
        landlord = self._landlord_repo.add_landlord(landlord)
        return landlord

    def get_flats(self) -> tuple[list[Flat], list[list[str]]]:
        flats = self._flat_repo.get_flats()
        photos = [self._flat_repo.get_photos(flat.id) for flat in flats]
        return flats, photos

    def get_landlord(self, landlord: int | str) -> Landlord:
        landlord = self._landlord_repo.get_landlord(landlord)
        return landlord

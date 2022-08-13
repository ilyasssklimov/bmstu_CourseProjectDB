from src.database.database import BaseDatabase
from src.model.flat import Flat
from src.model.landlord import Landlord
from src.model.tenant import Tenant
from src.model.neighborhood import Neighborhood
from src.repository.tenant import TenantRepository
from src.repository.landlord import LandlordRepository
from src.repository.flat import FlatRepository
from src.repository.neighborhood import NeighborhoodRepository


class AdminController:
    def __init__(self, db: BaseDatabase):
        self.__tenant_repo = TenantRepository(db)
        self.__landlord_repo = LandlordRepository(db)
        self.__flat_repo = FlatRepository(db)
        self.__neighborhood_repo = NeighborhoodRepository(db)

    # tenant methods
    def get_tenants(self) -> tuple[list[str], list[Tenant]]:
        headers = Tenant().get_names()
        tenants = self.__tenant_repo.get_tenants()
        return headers, tenants

    def add_tenant(self, tenant: Tenant) -> Tenant:
        new_tenant = self.__tenant_repo.add_tenant(tenant)
        return new_tenant

    def update_tenant(self, tenant: Tenant) -> Tenant:
        upd_tenant = self.__tenant_repo.update_tenant(tenant)
        return upd_tenant

    def delete_tenant(self, tenant_id: int) -> Tenant:
        del_tenant = self.__tenant_repo.delete_tenant(tenant_id)
        return del_tenant

    # landlord methods
    def get_landlords(self) -> tuple[list[str], list[Landlord]]:
        headers = Landlord().get_names()
        landlords = self.__landlord_repo.get_landlords()
        return headers, landlords

    def add_landlord(self, landlord: Landlord) -> Landlord:
        new_landlord = self.__landlord_repo.add_landlord(landlord)
        return new_landlord

    def update_landlord(self, landlord: Landlord) -> Landlord:
        upd_landlord = self.__landlord_repo.update_landlord(landlord)
        return upd_landlord

    def delete_landlord(self, landlord_id: int) -> Landlord:
        del_landlord = self.__landlord_repo.delete_landlord(landlord_id)
        return del_landlord

    def check_landlord(self, landlord_id: int) -> bool:
        return self.__landlord_repo.check_landlord(landlord_id)

    # flat methods
    def get_flats(self) -> (list[str], list[Flat]):
        headers = Flat().get_names()
        flats = self.__flat_repo.get_flats()
        return headers, flats

    def add_flat(self, flat: Flat) -> Flat:
        new_flat = self.__flat_repo.add_flat(flat)
        return new_flat

    def update_flat(self, flat: Flat) -> Flat:
        upd_flat = self.__flat_repo.update_flat(flat)
        return upd_flat

    def delete_flat(self, flat_id: int) -> Flat:
        del_flat = self.__flat_repo.delete_flat(flat_id)
        return del_flat

    # neighborhood methods
    def get_neighborhoods(self) -> (list[str], list[Neighborhood]):
        headers = Neighborhood().get_names()
        neighborhoods = self.__neighborhood_repo.get_neighborhoods()
        return headers, neighborhoods

    def add_neighborhood(self, neighborhood: Neighborhood) -> Neighborhood:
        new_neighborhood = self.__neighborhood_repo.add_neighborhood(neighborhood)
        return new_neighborhood

    def update_neighborhood(self, neighborhood: Neighborhood) -> Neighborhood:
        upd_neighborhood = self.__neighborhood_repo.update_neighborhood(neighborhood)
        return upd_neighborhood

    def delete_neighborhood(self, neighborhood_id: int) -> Neighborhood:
        del_neighborhood = self.__neighborhood_repo.delete_neighborhood(neighborhood_id)
        return del_neighborhood

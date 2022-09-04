from src.controller.guest import GuestController
from src.model.landlord import Landlord
from src.model.flat import Flat
from src.model.neighborhood import Neighborhood
from src.model.tenant import Tenant
from src.model.goods import Goods


class TenantController(GuestController):
    def get_flats_filters(self, price: tuple[int, int], rooms: tuple[int, int], square: tuple[float, float],
                          metro: list[str]) -> tuple[list[Flat], list[list[str]]]:
        flats = self._flat_repo.get_flats_filters(price, rooms, square, metro)
        photos = [self._flat_repo.get_photos(flat.id) for flat in flats]
        return flats, photos

    def update_landlord(self, landlord: Landlord) -> Landlord:
        upd_landlord = self._landlord_repo.update_landlord(landlord)
        return upd_landlord

    def subscribe_landlord(self, tenant_id: int, landlord_id: int) -> bool:
        result = self._tenant_repo.subscribe_landlord(tenant_id, landlord_id)
        return result

    def unsubscribe_landlord(self, tenant_id: int, landlord_id: int) -> bool:
        result = self._tenant_repo.unsubscribe_landlord(tenant_id, landlord_id)
        return result

    def check_subscription_landlord(self, tenant_id: int, landlord_id: int) -> bool:
        result = self._tenant_repo.check_subscription_landlord(tenant_id, landlord_id)
        return result

    def like_flat(self, tenant_id: int, flat_id: int) -> bool:
        result = self._tenant_repo.like_flat(tenant_id, flat_id)
        return result

    def unlike_flat(self, tenant_id: int, flat_id: int) -> bool:
        result = self._tenant_repo.unlike_flat(tenant_id, flat_id)
        return result

    def check_like_flat(self, tenant_id: int, flat_id: int) -> bool:
        result = self._tenant_repo.check_like_flat(tenant_id, flat_id)
        return result

    def get_likes_flat(self, flat_id: int) -> list[Tenant]:
        tenants = self._tenant_repo.get_likes_flat(flat_id)
        return tenants

    def subscribe_flat(self, tenant_id: int, price: tuple[int, int], rooms: tuple[int, int],
                       square: tuple[float, float], metro: list[str]) -> bool:
        result = self._tenant_repo.subscribe_flat(tenant_id, price, rooms, square, metro)
        return result

    def unsubscribe_flat(self, tenant_id: int) -> bool:
        result = self._tenant_repo.unsubscribe_flat(tenant_id)
        return result

    def add_neighborhood(self, neighborhood: Neighborhood) -> Neighborhood:
        new_neighborhood = self._neighborhood_repo.add_neighborhood(neighborhood)
        return new_neighborhood

    def get_neighborhoods_filters(self, neighbors: tuple[int, int], price: tuple[int, int],
                                  sex: str) -> list[Neighborhood]:
        neighborhoods = self._neighborhood_repo.get_neighborhoods_filters(neighbors, price, sex)
        return neighborhoods

    def add_goods(self, goods: Goods) -> Goods:
        new_goods = self._goods_repo.add_goods(goods)
        return new_goods

    def get_goods_filters(self, price: tuple[int, int], condition: str) -> list[Goods]:
        goods = self._goods_repo.get_goods_filters(price, condition)
        return goods

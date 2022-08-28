import abc
from multipledispatch import dispatch
from src.database.config import RolesDB


class BaseDatabase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def connect_db(self, db_params: dict[str, str]): ...

    @abc.abstractmethod
    def disconnect_db(self): ...

    @abc.abstractmethod
    def set_role(self, role: RolesDB): ...

    @abc.abstractmethod
    def execute(self, query: str): ...

    @abc.abstractmethod
    def select(self, query: str): ...

    # tenant methods
    @abc.abstractmethod
    def add_tenant(self, user_id: int, full_name: str, sex: str, city: str, qualities: str,
                   age: int, solvency: bool, username: str): ...

    @abc.abstractmethod
    def get_tenants(self): ...

    @abc.abstractmethod
    def get_tenant(self, tenant_id: int): ...

    @abc.abstractmethod
    def update_tenant(self, tenant_id: int, full_name: str, sex: str, city: str, qualities: str,
                      age: int, solvency: bool): ...

    @abc.abstractmethod
    def delete_tenant(self, tenant_id: int): ...

    @abc.abstractmethod
    def delete_tenants(self): ...

    @abc.abstractmethod
    def check_tenant(self, tenant_id: int): ...

    # landlord methods
    @abc.abstractmethod
    def add_landlord(self, user_id: int, full_name: str, city: str, rating: float, age: int,
                     phone: str, username: str): ...

    @abc.abstractmethod
    def get_landlords(self): ...

    @dispatch(int)
    @abc.abstractmethod
    def get_landlord(self, landlord_id: int): ...

    @dispatch(str)
    @abc.abstractmethod
    def get_landlord(self, landlord_name: str): ...

    @abc.abstractmethod
    def update_landlord(self, landlord_id: int, full_name: str, city: str, rating: float, age: int,
                        phone: str, username: str): ...

    @abc.abstractmethod
    def delete_landlord(self, landlord_id: int): ...

    @abc.abstractmethod
    def delete_landlords(self): ...

    @abc.abstractmethod
    def check_landlord(self, landlord_id: int): ...

    # flat methods
    @abc.abstractmethod
    def add_flat(self, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                 floor: int, max_floor: int, description: str): ...

    @abc.abstractmethod
    def get_flats(self): ...

    @abc.abstractmethod
    def get_flats_filters(self, price: tuple[int, int], rooms: tuple[int, int], square: tuple[float, float],
                          metro: list[str]): ...

    @abc.abstractmethod
    def add_photo(self, flat_id: int, photo: str): ...

    @abc.abstractmethod
    def delete_photos(self, flat_id: int): ...

    @abc.abstractmethod
    def get_photos(self, flat_id: int): ...

    @abc.abstractmethod
    def get_flat(self, flat_id: int): ...

    @abc.abstractmethod
    def delete_flat(self, flat_id: int): ...

    @abc.abstractmethod
    def delete_flats(self): ...

    @abc.abstractmethod
    def update_flat(self, flat_id: int, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                    floor: int, max_floor: int, description: str): ...

    # neighborhood methods
    @abc.abstractmethod
    def add_neighborhood(self, tenant_id: int, neighbors: int, price: int, place: str, sex: str, preferences: str): ...

    @abc.abstractmethod
    def get_neighborhoods(self): ...

    @abc.abstractmethod
    def get_neighborhoods_filters(self, neighbors: tuple[int, int], price: tuple[int, int], sex: str): ...

    @abc.abstractmethod
    def get_neighborhood(self, neighborhood_id: int): ...

    @abc.abstractmethod
    def update_neighborhood(self, neighborhood_id: int, tenant_id: int, neighbors: int, price: int,
                            place: str, sex: str, preferences: str): ...

    @abc.abstractmethod
    def delete_neighborhood(self, neighborhood_id: int): ...

    @abc.abstractmethod
    def delete_neighborhoods(self): ...

    # goods methods
    @abc.abstractmethod
    def add_goods(self, owner_id: int, name: str, price: int, condition: str, bargain: bool): ...

    @dispatch()
    @abc.abstractmethod
    def get_goods(self): ...

    @dispatch(int)
    @abc.abstractmethod
    def get_goods(self, goods_id: int): ...

    @abc.abstractmethod
    def update_goods(self, goods_id: int, owner_id: int, name: str, price: int, condition: str, bargain: bool): ...

    @dispatch(int)
    @abc.abstractmethod
    def delete_goods(self, goods_id: int): ...

    @dispatch()
    @abc.abstractmethod
    def delete_goods(self): ...

    @abc.abstractmethod
    def subscribe_landlord(self, tenant_id: int, landlord_id: int): ...

    @abc.abstractmethod
    def unsubscribe_landlord(self, tenant_id: int, landlord_id: int): ...

    @abc.abstractmethod
    def check_subscription_landlord(self, tenant_id: int, landlord_id: int): ...

    @abc.abstractmethod
    def get_tenants_subscription(self, landlord_id: int): ...

    @abc.abstractmethod
    def like_flat(self, tenant_id: int, flat_id: int): ...

    @abc.abstractmethod
    def unlike_flat(self, tenant_id: int, flat_id: int): ...

    @abc.abstractmethod
    def check_like_flat(self, tenant_id: int, flat_id: int): ...

    @abc.abstractmethod
    def get_likes_flat(self, flat_id: int): ...

    @abc.abstractmethod
    def subscribe_flat(self, tenant_id: int, price: tuple[int, int], rooms: tuple[int, int],
                       square: tuple[float, float], metro: list[str]): ...

    @abc.abstractmethod
    def unsubscribe_flat(self, tenant_id: int): ...

    @abc.abstractmethod
    def get_subscribed_flat_tenants(self, price: int, rooms: int, square: float, metro: str): ...

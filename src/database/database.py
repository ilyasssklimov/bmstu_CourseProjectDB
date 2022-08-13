import abc
from src.database.config import RolesDB


class BaseDatabase(metaclass=abc.ABCMeta):
    def connect_db(self, db_params: dict[str, str]):
        """
        Connect to database by params
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_role(self, role: RolesDB):
        """
        Set role to use database
        """
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, query: str):
        """
        Execute query
        """
        raise NotImplementedError

    @abc.abstractmethod
    def select(self, query: str):
        """
        Select by query
        """
        raise NotImplementedError

    # tenant methods
    @abc.abstractmethod
    def add_tenant(self, user_id: int, full_name: str, sex: str, city: str, qualities: str, age: int, solvency: bool):
        """
        Add tenant to database
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tenants(self):
        """
        Get all tenants
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tenant(self, tenant_id: int):
        """
        Get tenant by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_tenant(self, tenant_id: int, full_name: str, sex: str, city: str,
                      qualities: str, age: int, solvency: bool):
        """
        Update tenant by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_tenant(self, tenant_id: int):
        """
        Delete tenant by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def check_tenant(self, tenant_id: int):
        """
        Check by id if tenant exists in database
        """
        raise NotImplementedError

    # landlord methods
    @abc.abstractmethod
    def add_landlord(self, user_id: int, full_name: str, city: str, rating: float, age: int, phone: str, username: str):
        """
        Add landlord to database
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_landlords(self):
        """
        Get all landlords
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_landlord(self, landlord_id: int):
        """
        Get landlord by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_landlord(self, landlord_id: int, full_name: str, city: str, rating: float, age: int,
                        phone: str, username: str):
        """
        Update landlord by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_landlord(self, landlord_id: int):
        """
        Delete landlord by id
        """

    @abc.abstractmethod
    def check_landlord(self, landlord_id: int):
        """
        Check by id if landlord exists in database
        """
        raise NotImplementedError

    # flat methods
    @abc.abstractmethod
    def add_flat(self, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                 floor: int, max_floor: int, description: str):
        """
        Add flat to database
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_flats(self):
        """
        Get all flats
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_photo(self, flat_id: int, photo: str):
        """
        Add photo of flat
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_photos(self, flat_id: int):
        """
        Delete photos of flat by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_photos(self, flat_id: int):
        """
        Get photos of flat by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_flat(self, flat_id: int):
        """
        Get flat by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_flat(self, flat_id: int):
        """
        Delete flat by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_flat(self, flat_id: int, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                    floor: int, max_floor: int, description: str):
        """
        Update flat by id
        """
        raise NotImplementedError

    # neighborhood methods
    @abc.abstractmethod
    def add_neighborhood(self, tenant_id: int, neighbors: int, price: int, place: str, sex: str, preferences: str):
        """
        Add neighborhood to database
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_neighborhoods(self):
        """
        Get all neighborhoods
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_neighborhood(self, neighborhood_id: int):
        """
        Get neighborhood by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_neighborhood(self, neighborhood_id: int, tenant_id: int, neighbors: int, price: int,
                            place: str, sex: str, preferences: str):
        """
        Update neighborhood by id
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_neighborhood(self, neighborhood_id: int):
        """
        Delete neighborhood by id
        """
        raise NotImplementedError

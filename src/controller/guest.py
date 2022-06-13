import logging
import psycopg2 as ps

from src.database.database import PostgresDB
from src.model.flat import Flat
from src.model.tenant import Tenant
from src.model.landlord import Landlord


class GuestController:
    def __init__(self, db: PostgresDB):
        self._db = db

    def check_tenant(self, tenant_id: int):
        return self._db.check_tenant(tenant_id)

    def register_tenant(self, user_id: int, full_name: str, sex: str, city: str,
                        qualities: str, age: int, solvency: bool):
        try:
            self._db.add_tenant(user_id, full_name, sex, city, qualities, age, solvency)
            return Tenant(user_id, full_name, sex, city, qualities, age, solvency)
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while registration tenant with name \'{full_name}\'')
        return Tenant()

    def check_landlord(self, landlord_id: int):
        return self._db.check_landlord(landlord_id)

    def register_landlord(self, user_id: int, full_name: str, city: str, age: int, phone: str):
        rating = 0.0
        try:
            self._db.add_landlord(user_id, full_name, city, rating, age, phone)
            return Landlord(user_id, full_name, city, rating, age, phone)
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while registration landlord with name \'{full_name}\'')
        return Landlord()

    def get_flats(self):
        return [Flat(*flat[1:]) for flat in self._db.get_flats()]

    def get_landlord(self, landlord_id: int):
        landlord = Landlord(*self._db.get_landlord(landlord_id))
        if landlord:
            logging.info(f'Get landlord by id \'{landlord_id}\'')
            return landlord
        else:
            logging.error(f'Unable to get landlord by id = \'{landlord_id}\'')
            return None

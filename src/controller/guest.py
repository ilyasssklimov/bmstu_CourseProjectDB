import logging
import psycopg2 as ps

from src.database.database import PostgresDB
from src.model.tenant import Tenant


class GuestController:
    def __init__(self, db: PostgresDB):
        self.__db = db

    def check_tenant(self, user_id: int):
        return self.__db.check_tenant(user_id)

    def register_tenant(self, user_id: int, full_name: str, sex: str, city: str,
                        qualities: str, age: int, solvency: bool):
        try:
            self.__db.add_tenant(user_id, full_name, sex, city, qualities, age, solvency)
            return Tenant(user_id, full_name, sex, city, qualities, age, solvency)
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while registration tenant with name \'{full_name}\'')
            return Tenant()

import logging

import psycopg2 as ps
from src.database import PostgresDB


class GuestController:
    def __init__(self, db: PostgresDB):
        self.__db = db

    def register(self, full_name: str, sex: str, city: str, qualities: str, age: int, solvency: bool):
        try:
            self.__db.add_tenant(full_name, sex, city, qualities, age, solvency)
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while registration tenant with name \'{full_name}\'')

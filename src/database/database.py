import logging

import psycopg2 as ps
from config import DB_PARAMS, DB_TABLES_FILE, DB_CONSTRAINS_FILE
from model.tenant import Tenant


class PostgresDB:
    def __init__(self):
        self.__connection = None
        self.__cursor = None
        self.connect_db()
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINS_FILE)

    def connect_db(self):
        self.__connection = ps.connect(
            database=DB_PARAMS['database'],
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port']
        )
        self.__cursor = self.__connection.cursor()

    def close_db(self):
        self.__cursor.close()
        self.__connection.close()

    def execute(self, query):
        self.__cursor.execute(query)
        self.__connection.commit()

    def select(self, query):
        self.__cursor.execute(query)
        return self.__cursor.fetchall()

    def execute_file(self, filename):
        with open(filename) as f:
            self.execute(f.read())

    def add_tenant(self, full_name: str, sex: str, city: str, qualities: str, age: int, solvency: bool):
        query = f'''
        insert into say_no_to_hostel.public.tenant (full_name, sex, city, personal_qualities, age, solvency)
        values('{full_name}', '{sex}', '{city}', '{qualities}', {age}, {solvency});
        '''
        self.execute(query)
        logging.info(f'Tenant with name \'{full_name}\' is successfully added')
        return Tenant(full_name, sex, city, qualities, age, solvency)

    def get_users(self):
        query = '''select * from say_no_to_hostel.public.tenant;'''
        return self.select(query)

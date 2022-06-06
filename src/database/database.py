import logging
import psycopg2 as ps

from src.database.config import DB_TABLES_FILE, DB_CONSTRAINS_FILE


class PostgresDB:
    def __init__(self, db_params):
        self.__connection = None
        self.__cursor = None
        self.connect_db(db_params)
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINS_FILE)

    def connect_db(self, db_params):
        self.__connection = ps.connect(
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=db_params['port']
        )
        self.__cursor = self.__connection.cursor()

    def close_db(self):
        self.__cursor.close()
        self.__connection.close()

    def execute(self, query):
        try:
            self.__cursor.execute(query)
        except Exception as e:
            self.__connection.rollback()
            raise e
        self.__connection.commit()

    def select(self, query):
        try:
            self.__cursor.execute(query)
        except Exception as e:
            self.__connection.rollback()
            raise e
        return self.__cursor.fetchall()

    def execute_file(self, filename):
        try:
            with open(filename) as f:
                self.execute(f.read())
        except FileNotFoundError as e:
            logging.debug(e)

    def add_tenant(self, user_id: int, full_name: str, sex: str, city: str, qualities: str, age: int, solvency: bool):
        query = f'''
        INSERT INTO public.tenant (id, full_name, sex, city, personal_qualities, age, solvency)
        VALUES ({user_id}, '{full_name}', '{sex}', '{city}', '{qualities}', {age}, {solvency});
        '''
        self.execute(query)
        logging.info(f'Tenant with name \'{full_name}\' is successfully added')
        return user_id, full_name, sex, city, qualities, age, solvency

    def get_tenants(self):
        query = '''SELECT * FROM public.tenant'''
        logging.info('Get all users from DB')
        return self.select(query)

    def get_tenant(self, tenant_id):
        query = f'''SELECT * FROM public.tenant WHERE id = {tenant_id}'''
        return self.select(query)[0]

    def update_tenant(self, user_id: int, full_name: str, sex: str, city: str,
                      qualities: str, age: int, solvency: bool):
        query = f'''
        UPDATE public.tenant SET full_name = '{full_name}', sex = '{sex}', city = '{city}',
        personal_qualities = '{qualities}', age = {age}, solvency = {solvency} WHERE id = {user_id}
        '''
        logging.info(f'Update tenant with name = \'{full_name}\'')
        self.execute(query)
        return user_id, full_name, sex, city, qualities, age, solvency

    def delete_tenant(self, tenant_id):
        query = f'''DELETE FROM public.tenant WHERE id = {tenant_id};'''
        tenant = self.get_tenant(tenant_id)
        self.execute(query)
        logging.info(f'Delete tenant with id = {tenant_id}')
        return tenant

    def check_tenant(self, user_id: int):
        query = f'''SELECT * FROM public.tenant WHERE id = {user_id}'''
        users = self.select(query)
        logging.info('Checking tenants')
        return True if users else False

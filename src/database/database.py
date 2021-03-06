import logging
import psycopg2 as ps

from src.database.config import DB_TABLES_FILE, DB_CONSTRAINS_FILE, DB_ROLES_FILE, RolesDB


class PostgresDB:
    def __init__(self, db_params: dict):
        self.__connection = None
        self.__cursor = None
        self.connect_db(db_params)

    def execute_init_files(self):
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINS_FILE)
        self.execute_file(DB_ROLES_FILE)

    def connect_db(self, db_params: dict):
        self.__connection = ps.connect(**db_params)
        self.__cursor = self.__connection.cursor()

    def close_connection(self):
        self.__cursor.close()
        self.__connection.close()

    def set_role(self, role: RolesDB):
        query = f'SET ROLE {role.value}'
        self.execute(query)

    def execute(self, query: str):
        try:
            self.__cursor.execute(query)
        except Exception as e:
            self.__connection.rollback()
            raise e
        self.__connection.commit()

    def select(self, query: str):
        try:
            self.__cursor.execute(query)
        except Exception as e:
            self.__connection.rollback()
            raise e
        return self.__cursor.fetchall()

    def execute_file(self, filename: str):
        try:
            with open(filename) as f:
                self.execute(f.read())
        except FileNotFoundError as e:
            logging.debug(e)

    # tenant methods
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
        logging.info('Get all tenants from DB')
        return self.select(query)

    def get_tenant(self, tenant_id):
        query = f'''SELECT * FROM public.tenant WHERE id = {tenant_id}'''
        logging.info(f'Get tenant with id = {tenant_id}')
        return self.select(query)[0]

    def update_tenant(self, tenant_id: int, full_name: str, sex: str, city: str,
                      qualities: str, age: int, solvency: bool):
        query = f'''
        UPDATE public.tenant SET full_name = '{full_name}', sex = '{sex}', city = '{city}',
        personal_qualities = '{qualities}', age = {age}, solvency = {solvency} WHERE id = {tenant_id}
        '''
        logging.info(f'Update tenant with name = \'{full_name}\'')
        self.execute(query)
        return tenant_id, full_name, sex, city, qualities, age, solvency

    def delete_tenant(self, tenant_id):
        query = f'''DELETE FROM public.tenant WHERE id = {tenant_id};'''
        tenant = self.get_tenant(tenant_id)
        self.execute(query)
        logging.info(f'Delete tenant with id = {tenant_id}')
        return tenant

    def check_tenant(self, tenant_id: int):
        query = f'''SELECT * FROM public.tenant WHERE id = {tenant_id}'''
        tenants = self.select(query)
        logging.info('Checking tenants')
        return bool(tenants)

    # landlord methods
    def add_landlord(self, user_id: int, full_name: str, city: str, rating: float, age: int, phone: str, username: str):
        query = f'''
        INSERT INTO public.landlord (id, full_name, city, rating, age, phone, username)
        VALUES ({user_id}, '{full_name}', '{city}', {rating}, {age}, '{phone}', '{username}');
        '''
        self.execute(query)
        logging.info(f'Landlord with name \'{full_name}\' is successfully added')
        return user_id, full_name, city, rating, age

    def get_landlords(self):
        query = '''SELECT * FROM public.landlord'''
        logging.info('Get all landlords from DB')
        return self.select(query)

    def get_landlord(self, landlord_id):
        query = f'''SELECT * FROM public.landlord WHERE id = {landlord_id}'''
        logging.info(f'Get landlord with id = {landlord_id}')
        return self.select(query)[0]

    def update_landlord(self, landlord_id: int, full_name: str, city: str, rating: float, age: int):
        query = f'''
        UPDATE public.landlord SET full_name = '{full_name}', city = '{city}', rating = {rating}, age = {age} 
        WHERE id = {landlord_id}
        '''
        logging.info(f'Update landlord with name = \'{full_name}\'')
        self.execute(query)
        return landlord_id, full_name, city, rating, age

    def delete_landlord(self, landlord_id):
        query = f'''DELETE FROM public.landlord WHERE id = {landlord_id};'''
        landlord = self.get_landlord(landlord_id)
        self.execute(query)
        logging.info(f'Delete landlord with id = {landlord_id}')
        return landlord

    def check_landlord(self, landlord_id: int):
        query = f'''SELECT * FROM public.landlord WHERE id = {landlord_id}'''
        landlords = self.select(query)
        logging.info('Checking landlords')
        return bool(landlords)

    # flat methods
    def add_flat(self, owner_id: int, price: int, square: float, address: str, metro: str,
                 floor: int, max_floor: int, description: int):
        query = f'''
        INSERT INTO public.flat (owner_id, price, square, address, metro, floor, max_floor, description)
        VALUES ({owner_id}, {price}, {square}, '{address}', '{metro}', {floor}, {max_floor}, '{description}')
        '''
        self.execute(query)
        logging.info(f'Flat with owner_id \'{owner_id}\' is successfully added')
        flat_id = self.select('''SELECT CURRVAL('flat_id_seq');''')[0][0]
        return flat_id, owner_id, price, square, address, metro, floor, max_floor, description

    def get_flats(self):
        query = f'''SELECT * FROM public.flat'''
        logging.info('Get all flats')
        return self.select(query)

    def add_photo(self, flat_id: int, photo: str):
        query = f'''INSERT INTO public.flat_photo (flat_id, photo) VALUES ({flat_id}, '{photo}')'''
        self.execute(query)
        logging.info(f'Add photo to flat with id \'{flat_id}\'')
        return photo

    def get_flat_photos(self, flat_id: int):
        query = f'''SELECT photo FROM public.flat_photo WHERE flat_id = {flat_id}'''
        logging.info(f'Get photos of flat with id \'{flat_id}\'')
        return [photo[0] for photo in self.select(query)]

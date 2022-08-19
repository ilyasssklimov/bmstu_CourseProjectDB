import logging
from multipledispatch import dispatch
import psycopg2 as ps
from src.database.config import DB_TABLES_FILE, DB_CONSTRAINTS_FILE, DB_ROLES_FILE, DB_TRIGGER_FILE, RolesDB
from src.database.database import BaseDatabase


class PgDatabase(BaseDatabase):
    def __init__(self, db_params: dict[str, str]):
        self.__connection = None
        self.__cursor = None
        self.connect_db(db_params)
        self.execute_init_files()

    def execute_init_files(self):
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINTS_FILE)
        self.execute_file(DB_ROLES_FILE)
        self.execute_file(DB_TRIGGER_FILE)

    def connect_db(self, db_params: dict[str, str]):
        self.__connection = ps.connect(**db_params)
        self.__cursor = self.__connection.cursor()

    def disconnect_db(self):
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

    def get_landlord(self, landlord_id: int):
        query = f'''SELECT * FROM public.landlord WHERE id = {landlord_id}'''
        logging.info(f'Get landlord with id = {landlord_id}')
        return self.select(query)[0]

    def update_landlord(self, landlord_id: int, full_name: str, city: str, rating: float, age: int,
                        phone: str, username: str):
        query = f'''
        UPDATE public.landlord SET full_name = '{full_name}', city = '{city}', rating = {rating}, age = {age},
        phone = '{phone}', username = '{username}' WHERE id = {landlord_id}
        '''
        logging.info(f'Update landlord with name = \'{full_name}\'')
        self.execute(query)
        return landlord_id, full_name, city, rating, age

    def delete_landlord(self, landlord_id: int):
        query = f'''DELETE FROM public.landlord WHERE id = {landlord_id};'''
        landlord = self.get_landlord(landlord_id)
        self.execute(query)
        logging.info(f'Delete landlord with id = {landlord_id}')
        return landlord

    def check_landlord(self, landlord_id: int):
        query = f'''SELECT * FROM public.landlord WHERE id = {landlord_id}'''
        landlords = self.select(query)
        logging.info('Checking landlord')
        return bool(landlords)

    # flat methods
    def add_flat(self, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                 floor: int, max_floor: int, description: str):
        query = f'''
        INSERT INTO public.flat (owner_id, price, rooms, square, address, metro, floor, max_floor, description)
        VALUES ({owner_id}, {price}, {rooms}, {square}, '{address}', '{metro}', {floor}, {max_floor}, '{description}')
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

    def delete_photos(self, flat_id: int):
        query = f'''DELETE FROM public.flat_photo WHERE flat_id = {flat_id}'''
        photos = self.get_photos(flat_id)
        self.execute(query)
        logging.info(f'Delete photos of flat with id = {flat_id}')
        return photos

    def get_photos(self, flat_id: int):
        query = f'''SELECT photo FROM public.flat_photo WHERE flat_id = {flat_id}'''
        logging.info(f'Get photos of flat with id \'{flat_id}\'')
        return [photo[0] for photo in self.select(query)]

    def get_flat(self, flat_id: int):
        query = f'''SELECT * FROM public.flat WHERE id = {flat_id}'''
        logging.info(f'Get flat with id = {flat_id}')
        return self.select(query)[0]

    def delete_flat(self, flat_id: int):
        query = f'''DELETE FROM public.flat WHERE id = {flat_id};'''
        flat = self.get_flat(flat_id)
        photos = self.delete_photos(flat_id)
        self.execute(query)
        logging.info(f'Delete flat with id = {flat_id}')
        return flat, photos

    def update_flat(self, flat_id: int, owner_id: int, price: int, rooms: int, square: float, address: str, metro: str,
                    floor: int, max_floor: int, description: str):
        query = f'''
        UPDATE public.flat SET owner_id = {owner_id}, price = {price}, rooms = {rooms}, square = {square}, 
                               address = '{address}', metro = '{metro}', floor = {floor}, max_floor = {max_floor},
                               description = '{description}' 
        WHERE id = {flat_id}
        '''
        self.execute(query)
        logging.info(f'Update flat with id = \'{flat_id}\'')
        return flat_id, owner_id, price, rooms, square, address, metro, floor, max_floor, description

    # neighborhood methods
    def add_neighborhood(self, tenant_id: int, neighbors: int, price: int, place: str, sex: str, preferences: str):
        query = f'''
        INSERT INTO public.neighborhood (tenant_id, neighbors, price, place, sex, preferences)
        VALUES ({tenant_id}, {neighbors}, {price}, '{place}', '{sex}', '{preferences}')
        '''
        self.execute(query)
        logging.info(f'Neighborhood with tenant_id \'{tenant_id}\' is successfully added')
        neighborhood_id = self.select('''SELECT CURRVAL('neighborhood_id_seq');''')[0][0]
        return neighborhood_id, tenant_id, neighbors, price, place, sex, preferences

    def get_neighborhoods(self):
        query = f'''SELECT * FROM public.neighborhood'''
        logging.info('Get all neighborhood')
        return self.select(query)

    def get_neighborhood(self, neighborhood_id: int):
        query = f'''SELECT * FROM public.neighborhood WHERE id = {neighborhood_id}'''
        logging.info(f'Get neighborhood with id = {neighborhood_id}')
        return self.select(query)[0]

    def update_neighborhood(self, neighborhood_id: int, tenant_id: int, neighbors: int, price: int,
                            place: str, sex: str, preferences: str):
        query = f'''
        UPDATE public.neighborhood SET tenant_id = {tenant_id}, neighbors = {neighbors}, price = {price}, 
                                       place = '{place}', sex = '{sex}', preferences = '{preferences}' 
        WHERE id = {neighborhood_id}
        '''
        self.execute(query)
        logging.info(f'Update neighborhood with id = \'{neighborhood_id}\'')
        return neighborhood_id, tenant_id, neighbors, price, place, sex, preferences

    def delete_neighborhood(self, neighborhood_id: int):
        query = f'''DELETE FROM public.neighborhood WHERE id = {neighborhood_id};'''
        neighborhood = self.get_neighborhood(neighborhood_id)
        self.execute(query)
        logging.info(f'Delete neighborhood with id = {neighborhood_id}')
        return neighborhood

    # goods methods
    def add_goods(self, owner_id: int, name: str, price: int, condition: str, bargain: bool):
        query = f'''
        INSERT INTO public.goods (owner_id, name, price, condition, bargain)
        VALUES ({owner_id}, '{name}', {price}, '{condition}', {bargain})
        '''
        self.execute(query)
        logging.info(f'Goods with owner_id \'{owner_id}\' is successfully added')
        goods_id = self.select('''SELECT CURRVAL('goods_id_seq');''')[0][0]
        return goods_id, owner_id, name, price, condition, bargain

    @dispatch()
    def get_goods(self):
        query = f'''SELECT * FROM public.goods'''
        logging.info('Get all goods')
        return self.select(query)

    @dispatch(int)
    def get_goods(self, goods_id: int):
        query = f'''SELECT * FROM public.goods WHERE id = {goods_id}'''
        logging.info(f'Get goods with id = {goods_id}')
        return self.select(query)[0]

    def update_goods(self, goods_id: int, owner_id: int, name: str, price: int, condition: str, bargain: bool):
        query = f'''
        UPDATE public.goods SET owner_id = {owner_id}, name = '{name}', price = {price},
                                condition = '{condition}', bargain = {bargain} 
        WHERE id = {goods_id}
        '''
        self.execute(query)
        logging.info(f'Update goods with id = \'{goods_id}\'')
        return goods_id, owner_id, name, price, condition, bargain

    def delete_goods(self, goods_id: int):
        query = f'''DELETE FROM public.goods WHERE id = {goods_id};'''
        goods = self.get_goods(goods_id)
        self.execute(query)
        logging.info(f'Delete goods with id = {goods_id}')
        return goods

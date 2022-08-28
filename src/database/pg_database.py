import logging
from multipledispatch import dispatch
import psycopg2 as ps
from src.database.config import DB_TABLES_FILE, DB_CONSTRAINTS_FILE, DB_ROLES_FILE, DB_TRIGGERS_FILE, RolesDB
from src.database.database import BaseDatabase


class PgDatabase(BaseDatabase):
    def __init__(self, db_params: dict[str, str]):
        self.__connection, self.__cursor = None, None
        self.connect_db(db_params)
        self.execute_init_files()

    def execute_init_files(self):
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINTS_FILE)
        self.execute_file(DB_ROLES_FILE)
        self.execute_file(DB_TRIGGERS_FILE)

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
    def add_tenant(self, user_id: int, full_name: str, sex: str, city: str, qualities: str, age: int,
                   solvency: bool, username: str):
        query = f'''
        INSERT INTO public.tenant (id, full_name, sex, city, personal_qualities, age, solvency, username)
        VALUES ({user_id}, '{full_name}', '{sex}', '{city}', '{qualities}', {age}, {solvency}, '{username}');
        '''
        self.execute(query)
        logging.info(f'Tenant with name \'{full_name}\' is successfully added')
        return user_id, full_name, sex, city, qualities, age, solvency, username

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

    def delete_tenants(self):
        query = '''DELETE FROM public.tenant;'''
        tenants = self.get_tenants()
        self.execute(query)
        logging.info(f'Delete all tenants')
        return tenants

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

    @dispatch(int)
    def get_landlord(self, landlord_id: int):
        query = f'''SELECT * FROM public.landlord WHERE id = {landlord_id}'''
        logging.info(f'Get landlord with id = {landlord_id}')
        return self.select(query)[0]

    @dispatch(str)
    def get_landlord(self, landlord_name: str):
        query = f'''SELECT * FROM public.landlord WHERE username = '{landlord_name}' OR 
                                                        full_name = '{landlord_name}' '''
        logging.info(f'Get landlord with name = {landlord_name}')
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

    def delete_landlords(self):
        query = '''DELETE FROM public.landlord;'''
        landlords = self.get_landlords()
        self.execute(query)
        logging.info(f'Delete all landlords')
        return landlords

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
        return flat_id, owner_id, price, rooms, square, address, metro, floor, max_floor, description

    def get_flats(self):
        query = f'''SELECT * FROM public.flat'''
        logging.info('Get all flats')
        return self.select(query)

    def get_flats_filters(self, price: tuple[int, int], rooms: tuple[int, int], square: tuple[float, float],
                          metro: list[str]):
        query = f'''SELECT * FROM public.flat'''

        conditions = ''
        conditions += f'''price BETWEEN {price[0]} AND {price[1]} AND ''' if price else ''
        conditions += f'''rooms BETWEEN {rooms[0]} AND {rooms[1]} AND ''' if rooms else ''
        conditions += f'''square BETWEEN {square[0]} AND {square[1]} AND ''' if square else ''
        conditions = conditions.rstrip('AND ') if not metro else (
                conditions + 'metro IN (' + ', '.join([f'\'{station.strip()}\'' for station in metro]) + ')'
        )
        if conditions:
            query += ' WHERE ' + conditions

        logging.info('Get flats by filters')
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
        self.execute(query)
        logging.info(f'Delete flat with id = {flat_id}')
        return flat

    def delete_flats(self):
        query = f'''DELETE FROM public.flat;'''
        flats = self.get_flats()
        self.execute(query)
        logging.info(f'Delete all flats')
        return flats

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

    def get_neighborhoods_filters(self, neighbors: tuple[int, int], price: tuple[int, int], sex: str):
        query = f'''SELECT * FROM public.neighborhood'''

        conditions = ''
        conditions += f'''neighbors BETWEEN {neighbors[0]} AND {neighbors[1]} AND ''' if neighbors else ''
        conditions += f'''price BETWEEN {price[0]} AND {price[1]} AND ''' if price else ''
        conditions += f'''sex = {sex} AND ''' if sex else ''
        conditions = conditions.rstrip('AND ')
        if conditions:
            query += ' WHERE ' + conditions

        logging.info('Get neighborhoods by filters')
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

    def delete_neighborhoods(self):
        query = f'''DELETE FROM public.neighborhood;'''
        neighborhoods = self.get_neighborhoods()
        self.execute(query)
        logging.info('Delete all neighborhoods')
        return neighborhoods

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

    @dispatch(int)
    def delete_goods(self, goods_id: int):
        query = f'''DELETE FROM public.goods WHERE id = {goods_id};'''
        goods = self.get_goods(goods_id)
        self.execute(query)
        logging.info(f'Delete goods with id = {goods_id}')
        return goods

    @dispatch()
    def delete_goods(self):
        query = f'''DELETE FROM public.goods;'''
        goods = self.get_goods()
        self.execute(query)
        logging.info('Delete all goods')
        return goods

    def subscribe_landlord(self, tenant_id: int, landlord_id: int):
        query = f'''
        INSERT INTO public.subscription_landlord (tenant_id, landlord_id)
        VALUES ({tenant_id}, {landlord_id})'''
        self.execute(query)
        logging.info(f'Add subscription of tenant with id = {tenant_id} to landlord with id = {landlord_id}')

    def unsubscribe_landlord(self, tenant_id: int, landlord_id: int):
        query = f'''
        DELETE FROM public.subscription_landlord WHERE tenant_id = {tenant_id} AND landlord_id = {landlord_id}'''
        self.execute(query)
        logging.info(f'Delete subscription of tenant with id = {tenant_id} to landlord with id = {landlord_id}')

    def check_subscription_landlord(self, tenant_id: int, landlord_id: int):
        query = f'''SELECT * FROM public.subscription_landlord 
                    WHERE tenant_id = {tenant_id} AND landlord_id = {landlord_id}'''
        subscription = self.select(query)
        logging.info(f'Checking subscription (tenant_id = {tenant_id}, landlord_id = {landlord_id}')
        return bool(subscription)

    def get_tenants_subscription(self, landlord_id: int):
        query = f'''
        SELECT * FROM public.tenant WHERE id IN (
            SELECT tenant_id FROM public.subscription_landlord WHERE landlord_id = {landlord_id}
        )'''
        logging.info(f'Get tenants subscribed on landlord with id = {landlord_id}')
        return self.select(query)

    def like_flat(self, tenant_id: int, flat_id: int):
        query = f'''
        INSERT INTO public.likes_flat (tenant_id, flat_id)
        VALUES ({tenant_id}, {flat_id})'''
        self.execute(query)
        logging.info(f'Add like of tenant with id = {tenant_id} to flat with id = {flat_id}')

    def unlike_flat(self, tenant_id: int, flat_id: int):
        query = f'''
        DELETE FROM public.likes_flat WHERE tenant_id = {tenant_id} AND flat_id = {flat_id}'''
        self.execute(query)
        logging.info(f'Delete like of tenant with id = {tenant_id} to flat with id = {flat_id}')

    def check_like_flat(self, tenant_id: int, flat_id: int):
        query = f'''SELECT * FROM public.likes_flat 
                    WHERE tenant_id = {tenant_id} AND flat_id = {flat_id}'''
        like = self.select(query)
        logging.info(f'Checking like (tenant_id = {tenant_id}, flat_id = {flat_id}')
        return bool(like)

    def get_likes_flat(self, flat_id: int):
        query = f'''
        SELECT * FROM public.tenant WHERE id IN (
            SELECT tenant_id FROM public.likes_flat WHERE flat_id = {flat_id}
        )'''
        logging.info(f'Get tenants liked flat with id = {flat_id}')
        return self.select(query)

    def subscribe_flat(self, tenant_id: int, price: tuple[int, int], rooms: tuple[int, int],
                       square: tuple[float, float], metro: list[str]):
        query = f'''INSERT INTO public.subscription_flat (tenant_id) VALUES ({tenant_id})'''
        self.execute(query)

        values = ''
        values += f'''min_price = {price[0]}, max_price = {price[1]}, ''' if price else ''
        values += f'''min_rooms = {rooms[0]}, max_rooms = {rooms[1]}, ''' if rooms else ''
        values += f'''min_square = {square[0]}, max_square = {square[1]}, ''' if square else ''
        values = values.rstrip(', ')
        if values:
            query = f'''UPDATE public.subscription_flat SET {values} WHERE tenant_id = {tenant_id}'''
            self.execute(query)

        for station in metro:
            query = f'''INSERT INTO public.subscription_metro (tenant_id, metro) 
            VALUES ({tenant_id}, '{station.strip()}')'''
            self.execute(query)
        if not metro:
            query = f'''INSERT INTO public.subscription_metro (tenant_id) VALUES ({tenant_id})'''
            self.execute(query)

        logging.info(f'Add subscription of tenant with id = {tenant_id} to flats')

    def unsubscribe_flat(self, tenant_id: int):
        query = f'''
        DELETE FROM public.subscription_flat WHERE tenant_id = {tenant_id}'''
        self.execute(query)
        logging.info(f'Delete subscription of tenant with id = {tenant_id} to flats')

    def get_subscribed_flat_tenants(self, price: int, rooms: int, square: float, metro: str):
        query = f'''
        SELECT t.id, t.full_name, t.sex, t.city, t.personal_qualities, t.age, t.solvency
        FROM public.subscription_flat f JOIN public.subscription_metro m 
        ON f.tenant_id = m.tenant_id
        JOIN public.tenant t ON f.tenant_id = t.id 
        WHERE ((f.min_price IS NULL OR f.max_price IS NULL OR ({price} BETWEEN f.min_price AND f.max_price)) AND 
               (f.min_rooms IS NULL OR f.max_rooms IS NULL OR ({rooms} BETWEEN f.min_rooms AND f.max_rooms)) AND 
               (f.min_square IS NULL OR f.max_square IS NULL OR ({square} BETWEEN f.min_square AND f.max_square)) AND 
               (m.metro IS NULL OR m.metro = '{metro}')
               )'''
        return self.select(query)

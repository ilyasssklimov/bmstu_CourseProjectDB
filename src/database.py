import psycopg2 as ps
from config import DB_PARAMS


class PostgresDB:
    def __init__(self):
        self.connection = None
        self.connect_db()

    def connect_db(self):
        self.connection = ps.connect(
            database=DB_PARAMS['database'],
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port']
        )

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def select(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def add_user(self, full_name, sex, city, qualities, age, solvency):
        query = f'''     
        insert into say_no_to_hostel.public.tenant (full_name, sex, city, personal_qualities, age, solvency)
        values(\'{full_name}\', \'{sex}\', \'{city}\', \'{qualities}\', \'{age}\', \'{solvency}\');
        '''
        self.execute(query)

    def get_user(self):
        query = '''select * from say_no_to_hostel.public.tenant;'''
        return self.select(query)

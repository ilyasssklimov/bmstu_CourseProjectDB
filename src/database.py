import psycopg2 as ps
from config import DB_PARAMS, DB_TABLES_FILE, DB_CONSTRAINS_FILE


class PostgresDB:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect_db()
        self.execute_file(DB_TABLES_FILE)
        self.execute_file(DB_CONSTRAINS_FILE)

    def connect_db(self):
        self.connection = ps.connect(
            database=DB_PARAMS['database'],
            user=DB_PARAMS['user'],
            password=DB_PARAMS['password'],
            host=DB_PARAMS['host'],
            port=DB_PARAMS['port']
        )
        self.cursor = self.connection.cursor()

    def close_db(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_file(self, filename):
        with open(filename) as f:
            self.execute(f.read())

    def add_user(self, full_name, sex, city, qualities, age, solvency):
        query = f'''     
        insert into say_no_to_hostel.public.tenant (full_name, sex, city, personal_qualities, age, solvency)
        values(\'{full_name}\', \'{sex}\', \'{city}\', \'{qualities}\', \'{age}\', \'{solvency}\');
        '''
        self.execute(query)

    def get_user(self):
        query = '''select * from say_no_to_hostel.public.tenant;'''
        return self.select(query)

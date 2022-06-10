API_TOKEN = '5170014779:AAGPyMd-QuEQge5jdWUwBO6Jg4kg_FcLrQY'

LOG_LEVEL = 'INFO'
LOG_FOLDER = 'log'
LOG_NAME_FILE = 'bot.log'


DB_DEFAULT_PARAMS = {
    'database': 'say_no_to_hostel',
    'user': 'postgres',
    'password': 'qwertyuiop',
    'host': 'localhost',
    'port': 5432
}

DB_ADMIN_PARAMS = {
    'database': 'say_no_to_hostel',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}

DB_GUEST_PARAMS = {
    'database': 'say_no_to_hostel',
    'user': 'guest',
    'password': 'guest',
    'host': 'localhost',
    'port': 5432
}


DB_TABLES_FILE = './query/tables.sql'
DB_CONSTRAINS_FILE = './query/constrains.sql'
DB_ROLES_FILE = './query/roles.sql'

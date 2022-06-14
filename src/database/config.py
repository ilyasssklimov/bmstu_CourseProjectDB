API_TOKEN = '5170014779:AAGPyMd-QuEQge5jdWUwBO6Jg4kg_FcLrQY'

LOG_LEVEL = 'INFO'
LOG_FOLDER = 'log'
LOG_NAME_FILE = 'bot.log'


DB_PARAMS = {'database': 'say_no_to_hostel', 'host': 'localhost', 'port': 5432}

DB_DEFAULT_PARAMS = {**DB_PARAMS, 'user': 'postgres', 'password': 'qwertyuiop'}
DB_GUEST_PARAMS = {**DB_PARAMS, 'user': 'guest', 'password': 'guest'}
DB_TENANT_PARAMS = {**DB_PARAMS, 'user': 'tenant', 'password': 'tenant'}
DB_LANDLORD_PARAMS = {**DB_PARAMS, 'user': 'landlord', 'password': 'labdlord'}
DB_ADMIN_PARAMS = {**DB_PARAMS, 'user': 'admin', 'password': 'admin'}


DB_TABLES_FILE = './query/tables.sql'
DB_CONSTRAINS_FILE = './query/constrains.sql'
DB_ROLES_FILE = './query/roles.sql'


IMG_PATH = './img'

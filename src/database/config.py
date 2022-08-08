from enum import Enum


class RolesDB(Enum):
    GUEST = 'guest'
    TENANT = 'tenant'
    LANDLORD = 'landlord'
    ADMIN = 'admin'


DB_PARAMS = {'database': 'say_no_to_hostel', 'host': 'localhost', 'port': 5432}

DB_DEFAULT_PARAMS = {**DB_PARAMS, 'user': 'postgres', 'password': 'qwertyuiop'}
DB_GUEST_PARAMS = {**DB_PARAMS, 'user': 'guest', 'password': 'guest'}
DB_TENANT_PARAMS = {**DB_PARAMS, 'user': 'tenant', 'password': 'tenant'}
DB_LANDLORD_PARAMS = {**DB_PARAMS, 'user': 'landlord', 'password': 'labdlord'}
DB_ADMIN_PARAMS = {**DB_PARAMS, 'user': 'admin', 'password': 'admin'}


DB_TABLES_FILE = './query/tables.sql'
DB_CONSTRAINTS_FILE = './query/constraints.sql'
DB_ROLES_FILE = './query/roles.sql'
DB_TRIGGER_FILE = './query/triggers.sql'

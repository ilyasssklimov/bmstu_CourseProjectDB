from src.generate_data.user import generate_tenants
from src.database.database import PostgresDB
from src.database.config import DB_ADMIN_PARAMS


def main():
    db = PostgresDB(DB_ADMIN_PARAMS)
    generate_tenants(db)


if __name__ == '__main__':
    main()

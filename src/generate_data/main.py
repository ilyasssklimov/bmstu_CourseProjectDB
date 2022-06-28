from src.bot.config import EntityTypes as Types
from src.database.database import PostgresDB
from src.database.config import DB_ADMIN_PARAMS
from src.generate_data.user import GenerateData


def main():
    db = PostgresDB(DB_ADMIN_PARAMS)
    generate = GenerateData(db)
    generate.generate_users(Types.TENANT)
    generate.generate_users(Types.LANDLORD)


if __name__ == '__main__':
    main()

from src.bot.config import EntityTypes as Types
from src.database.database import PostgresDB
from src.database.config import DB_ADMIN_PARAMS
from src.generate_data.user import GenerateData
from src.generate_data.flat import ParseFlats
from src.generate_data.config import MOSCOW_FLATS_URL


def main():
    db = PostgresDB(DB_ADMIN_PARAMS)
    generate = GenerateData(db)
    generate.generate_users(Types.TENANT)
    generate.generate_users(Types.LANDLORD)

    parse = ParseFlats(db)
    parse.add_flats(MOSCOW_FLATS_URL)


if __name__ == '__main__':
    main()

from aiogram import executor
import sys
sys.path.append('.')

from bot.bot import SayNoToHostelBot
from src.logger.logger import init_logger
from src.logger.config import TargetType
from src.database.config import DB_DEFAULT_PARAMS, RolesDB
from src.database.pg_database import PgDatabase


def main():
    init_logger(TargetType.BOT)
    SayNoToHostelBot.init_img_directory()

    database = PgDatabase(DB_DEFAULT_PARAMS)
    SayNoToHostelBot.init_db(database)
    SayNoToHostelBot.set_role(RolesDB.GUEST)

    executor.start_polling(SayNoToHostelBot.dispatcher, skip_updates=True)
    SayNoToHostelBot.close_db()


if __name__ == '__main__':
    main()

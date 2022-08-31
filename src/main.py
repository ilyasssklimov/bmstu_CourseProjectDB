from aiogram import executor
import sys
sys.path.append('.')

from bot.bot import SayNoToHostelBot
from src.logger.logger import init_logger
from src.logger.config import TargetType
from src.database.config import DB_DEFAULT_PARAMS, RolesDB
from src.database.pg_database import PgDatabase


def main():
    database = PgDatabase(DB_DEFAULT_PARAMS, init_files=True)
    database.disconnect_db()

    init_logger(TargetType.BOT)
    SayNoToHostelBot.init_img_directory()

    executor.start_polling(SayNoToHostelBot.dispatcher, skip_updates=True)
    SayNoToHostelBot.close_db()


if __name__ == '__main__':
    main()

from aiogram import executor
from bot.bot import SayNoToHostelBot
from bot.logger import init_logger
import sys

from src.database.config import RolesDB


def main():
    sys.path.append('.')
    init_logger()

    SayNoToHostelBot.init_img_directory()
    SayNoToHostelBot.execute_init_files()
    SayNoToHostelBot.set_role(RolesDB.GUEST)

    executor.start_polling(SayNoToHostelBot.dispatcher, skip_updates=True)
    SayNoToHostelBot.close_db()


if __name__ == '__main__':
    main()

from aiogram import executor
import sys
from bot.bot import SayNoToHostelBot
from src.logger.logger import init_logger
from src.logger.config import TargetType
from src.database.config import RolesDB


def main():
    sys.path.append('.')
    init_logger(TargetType.BOT)

    SayNoToHostelBot.init_img_directory()
    SayNoToHostelBot.execute_init_files()
    SayNoToHostelBot.set_role(RolesDB.GUEST)

    executor.start_polling(SayNoToHostelBot.dispatcher, skip_updates=True)
    SayNoToHostelBot.close_db()


if __name__ == '__main__':
    main()

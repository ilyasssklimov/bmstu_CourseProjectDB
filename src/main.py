from aiogram import executor
from bot.bot import dispatcher
from bot.logger import init_logger
import sys


if __name__ == '__main__':
    sys.path.append('.')
    init_logger()
    executor.start_polling(dispatcher, skip_updates=True)

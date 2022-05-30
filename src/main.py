from aiogram import executor
from bot import dispatcher
from logger import init_logger


if __name__ == '__main__':
    init_logger()
    executor.start_polling(dispatcher, skip_updates=True)

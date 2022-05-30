import logging

import psycopg2
from aiogram import Bot, Dispatcher, types
from config import API_TOKEN
from database import PostgresDB


bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)
try:
    database = PostgresDB()
except psycopg2.OperationalError:
    logging.error('Error! Unable to connect to database')


@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info('Starting bot')
    await message.reply('Привет! Я помогу тебе найти соседей, выбери действие :)')


@dispatcher.message_handler(commands=['register'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id, 'Давай зарегистрируемся!')


@dispatcher.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


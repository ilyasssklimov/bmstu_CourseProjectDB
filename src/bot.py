import logging
import psycopg2 as ps
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from config import API_TOKEN
from database import PostgresDB
from controller.guest import GuestController
from keyboard import register_keyboard, sex_keyboard, solvency_keyboard
from states import RegisterStates


bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
try:
    database = PostgresDB()
except ps.OperationalError:
    logging.error('Error! Unable to connect to database')
guest_controller = GuestController(database)


async def register_form(user_id: int):
    await bot.send_message(user_id, 'Заполните данные о себе:', reply_markup=register_keyboard)


@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info('Starting bot')
    await message.reply('Привет! Я помогу тебе найти соседей, выбери действие :)')


@dispatcher.message_handler(commands=['register'])
async def send_register(message: types.Message):
    await RegisterStates.START_STATE.set()
    await register_form(message.from_user.id)


@dispatcher.callback_query_handler(state=RegisterStates.START_STATE, text_contains='register')
async def register(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'register_name':
            await RegisterStates.NAME_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите полное имя:')
        case 'register_sex':
            await RegisterStates.SEX_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Укажите пол:', reply_markup=sex_keyboard)
        case 'register_city':
            await RegisterStates.CITY_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите город:')
        case 'register_qualities':
            await RegisterStates.QUALITIES_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите персональные качества:')
        case 'register_age':
            await RegisterStates.AGE_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите возраст:')
        case 'register_solvency':
            await RegisterStates.SOLVENCY_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Укажите, являетесь ли вы платежеспособным:',
                                   reply_markup=solvency_keyboard)
        case 'register_finish':
            async with state.proxy() as data:
                try:
                    full_name, sex, city, age = data['name'], data['sex'], data['city'], data['age']
                except KeyError:
                    await bot.send_message(callback_query.from_user.id, 'Обязательными полями для ввода являются: '
                                                                        'Имя, Пол, Город, Возраст')
                else:
                    try:
                        qualities, solvency = data['qualities'], data['solvency']
                    except KeyError:
                        qualities, solvency = '', 'null'
                    finally:
                        guest_controller.register(full_name, sex, city, qualities, age, solvency)
                        await state.finish()
                        await bot.send_message(callback_query.from_user.id, 'Регистрация успешно завершена')
        case _:
            await bot.answer_callback_query(callback_query.id)


async def input_register_str(message: types.Message, state: FSMContext, field: str):
    await RegisterStates.START_STATE.set()
    async with state.proxy() as data:
        data[field] = message.text
    await register_form(message.from_user.id)


@dispatcher.message_handler(state=RegisterStates.NAME_STATE)
async def input_name(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'name')


@dispatcher.message_handler(state=RegisterStates.CITY_STATE)
async def input_city(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'city')


@dispatcher.message_handler(state=RegisterStates.QUALITIES_STATE)
async def input_qualities(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'qualities')


@dispatcher.callback_query_handler(state=RegisterStates.SEX_STATE, text_contains='sex')
async def input_sex(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'sex_male' | 'sex_female':
            await RegisterStates.START_STATE.set()
            async with state.proxy() as data:
                data['sex'] = 'M' if callback_query.data == 'sex_male' else 'F'
            await bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id)
        case _:
            await bot.answer_callback_query(callback_query.id)


@dispatcher.message_handler(state=RegisterStates.AGE_STATE)
async def input_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        assert 14 <= age <= 100
    except ValueError:
        await bot.send_message(message.from_user.id, 'Возраст должен являться целым положительным числом')
    except AssertionError:
        await bot.send_message(message.from_user.id, 'Возраст не может быть меньше 14 и больше 100')
    else:
        async with state.proxy() as data:
            data['age'] = age
    finally:
        await RegisterStates.START_STATE.set()
        await register_form(message.from_user.id)


@dispatcher.callback_query_handler(state=RegisterStates.SOLVENCY_STATE, text_contains='solvency')
async def input_solvency(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'solvency_yes' | 'solvency_no':
            await RegisterStates.START_STATE.set()
            async with state.proxy() as data:
                data['solvency'] = True if callback_query.data == 'solvency_yes' else False
            await bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id)
        case _:
            await bot.answer_callback_query(callback_query.id)


@dispatcher.message_handler()
async def last_handler(message: types.Message):
    await message.answer('Вы ввели что-то неверное, для получения информации введите /help')

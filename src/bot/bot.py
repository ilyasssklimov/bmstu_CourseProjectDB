import logging
import psycopg2 as ps
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from src.database.config import API_TOKEN, DB_PARAMS
from src.database.database import PostgresDB
from src.controller.guest import GuestController
from src.bot.keyboard import register_tenant_keyboard, sex_keyboard, solvency_keyboard
from src.bot.states import RegisterTenantStates


bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

try:
    database = PostgresDB(DB_PARAMS)
except ps.OperationalError:
    logging.error('Error! Unable to connect to database')
    raise ValueError('Invalid params to connect to DB')

guest_controller = GuestController(database)


async def register_form(user_id: int):
    await bot.send_message(user_id, 'Заполните данные о себе:', reply_markup=register_tenant_keyboard)


@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info('Starting bot')
    await message.reply('Привет! Я помогу тебе найти соседей, выбери действие :)')


@dispatcher.message_handler(commands=['register_tenant'])
async def send_register(message: types.Message):
    user_id = message.from_user.id
    if guest_controller.check_tenant(user_id):
        await bot.send_message(user_id, 'Вы уже зарегистрированы как арендатор')
    else:
        await RegisterTenantStates.START_STATE.set()
        await register_form(user_id)


@dispatcher.callback_query_handler(state=RegisterTenantStates.START_STATE, text_contains='register_tenant')
async def register_tenant(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'register_tenant_name':
            await RegisterTenantStates.NAME_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите полное имя:')
        case 'register_tenant_sex':
            await RegisterTenantStates.SEX_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Укажите пол:', reply_markup=sex_keyboard)
        case 'register_tenant_city':
            await RegisterTenantStates.CITY_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите город:')
        case 'register_tenant_qualities':
            await RegisterTenantStates.QUALITIES_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите персональные качества:')
        case 'register_tenant_age':
            await RegisterTenantStates.AGE_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Введите возраст:')
        case 'register_tenant_solvency':
            await RegisterTenantStates.SOLVENCY_STATE.set()
            await bot.send_message(callback_query.from_user.id, 'Укажите, являетесь ли вы платежеспособным:',
                                   reply_markup=solvency_keyboard)
        case 'register_tenant_finish':
            async with state.proxy() as data:
                blank = []
                if 'name' not in data:
                    blank.append('Имя')
                if 'sex' not in data:
                    blank.append('Пол')
                if 'city' not in data:
                    blank.append('Город')
                if 'age' not in data:
                    blank.append('Возраст')

                if blank:
                    await bot.send_message(callback_query.from_user.id, 'Обязательными полями для ввода являются: ' +
                                                                        ', '.join(blank))
                    await register_form(callback_query.from_user.id)
                else:
                    full_name, sex, city, age = data['name'], data['sex'], data['city'], data['age']
                    qualities = data['qualities'] if 'qualities' in data else ''
                    solvency = data['solvency'] if 'solvency' in data else 'null'

                    tenant = guest_controller.register_tenant(callback_query.from_user.id, full_name, sex,
                                                              city, qualities, age, solvency)
                    if tenant:
                        await state.finish()
                        await bot.send_message(callback_query.from_user.id, 'Регистрация успешно завершена')
                    else:
                        await bot.send_message(callback_query.from_user.id, 'Во время регистрации произошла ошибка')
        case _:
            await bot.answer_callback_query(callback_query.id)


async def input_register_str(message: types.Message, state: FSMContext, field: str):
    await RegisterTenantStates.START_STATE.set()
    async with state.proxy() as data:
        data[field] = message.text
    await register_form(message.from_user.id)


@dispatcher.message_handler(state=RegisterTenantStates.NAME_STATE)
async def input_name(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'name')


@dispatcher.message_handler(state=RegisterTenantStates.CITY_STATE)
async def input_city(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'city')


@dispatcher.message_handler(state=RegisterTenantStates.QUALITIES_STATE)
async def input_qualities(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'qualities')


@dispatcher.callback_query_handler(state=RegisterTenantStates.SEX_STATE, text_contains='sex')
async def input_sex(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'sex_male' | 'sex_female':
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['sex'] = 'M' if callback_query.data == 'sex_male' else 'F'
            await bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id)
        case _:
            await bot.answer_callback_query(callback_query.id)


@dispatcher.message_handler(state=RegisterTenantStates.AGE_STATE)
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
        await RegisterTenantStates.START_STATE.set()
        await register_form(message.from_user.id)


@dispatcher.callback_query_handler(state=RegisterTenantStates.SOLVENCY_STATE, text_contains='solvency')
async def input_solvency(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'solvency_yes' | 'solvency_no':
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['solvency'] = True if callback_query.data == 'solvency_yes' else False
            await bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id)
        case _:
            await bot.answer_callback_query(callback_query.id)


@dispatcher.message_handler()
async def last_handler(message: types.Message):
    await message.answer('Вы ввели что-то неверное, для получения информации введите /help')

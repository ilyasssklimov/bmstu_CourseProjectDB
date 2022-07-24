from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup
import logging
import os

from src.bot.config import API_TOKEN, IMG_PATH, EntityTypes
from src.database.config import DB_DEFAULT_PARAMS, RolesDB
from src.database.database import PostgresDB
from src.controller.guest import GuestController
from src.controller.tenant import TenantController
from src.controller.landlord import LandlordController
import src.bot.keyboard as kb
from src.bot.message import MESSAGE_START, MESSAGE_HELP
from src.bot.states import RegisterTenantStates, RegisterLandlordStates, AddFlatStates


class SayNoToHostelBot:
    bot = Bot(token=API_TOKEN)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    database = PostgresDB(DB_DEFAULT_PARAMS)
    controller = None
    role = None
    controllers_dict = {
        RolesDB.GUEST: GuestController,
        RolesDB.TENANT: TenantController,
        RolesDB.LANDLORD: LandlordController
    }

    @classmethod
    def execute_init_files(cls):
        cls.database.execute_init_files()

    @classmethod
    def set_role(cls, role: RolesDB):
        if not isinstance(role, RolesDB):
            raise ValueError('You need use object of RolesDB to set role')

        cls.role = role
        cls.database.set_role(role)
        if role in cls.controllers_dict:
            cls.controller = cls.controllers_dict[role](cls.database)
        else:
            raise ValueError(f'There is no such role \'{role}\'')

    @classmethod
    def check_tenant(cls, user_id):
        check_res = cls.controller.check_tenant(user_id)
        if check_res:
            cls.set_role(RolesDB.TENANT)
        return check_res

    @classmethod
    def check_landlord(cls, user_id):
        check_res = cls.controller.check_landlord(user_id)
        if check_res:
            cls.set_role(RolesDB.LANDLORD)
        return check_res

    @staticmethod
    def init_img_directory():
        if not os.path.exists(IMG_PATH):
            os.makedirs(IMG_PATH)


@SayNoToHostelBot.dispatcher.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    SayNoToHostelBot.check_tenant(user_id)
    SayNoToHostelBot.check_landlord(user_id)

    logging.info('Starting bot')
    await SayNoToHostelBot.bot.send_message(user_id, MESSAGE_START)


@SayNoToHostelBot.dispatcher.message_handler(commands='help')
async def send_help(message: types.Message):
    await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)


async def register_form(user_id: int, keyboard: InlineKeyboardMarkup):
    await SayNoToHostelBot.bot.send_message(user_id, 'Заполните данные о себе:', reply_markup=keyboard)


@SayNoToHostelBot.dispatcher.message_handler(commands=['register_tenant', 'register_landlord'])
async def send_register(message: types.Message):
    user_id = message.from_user.id
    if message.text.endswith('tenant'):
        if SayNoToHostelBot.check_tenant(user_id):
            await SayNoToHostelBot.bot.send_message(user_id, 'Вы уже зарегистрированы как арендатор')
        else:
            await RegisterTenantStates.START_STATE.set()
            await register_form(user_id, kb.get_register_tenant_keyboard())
    elif message.text.endswith('landlord'):
        if SayNoToHostelBot.check_landlord(user_id):
            await SayNoToHostelBot.bot.send_message(user_id, 'Вы уже зарегистрированы как арендодатель')
        else:
            await RegisterLandlordStates.START_STATE.set()
            await register_form(user_id, kb.get_register_landlord_keyboard())


@SayNoToHostelBot.dispatcher.callback_query_handler(
    state=[RegisterTenantStates.START_STATE, RegisterLandlordStates.START_STATE], text_contains='register')
async def register_tenant(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'register_tenant_name' | 'register_landlord_name' as register_name:
            if 'tenant' in register_name:
                await RegisterTenantStates.NAME_STATE.set()
            elif 'landlord' in register_name:
                await RegisterLandlordStates.NAME_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите полное имя:')

        case 'register_tenant_sex':
            await RegisterTenantStates.SEX_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите пол:',
                                                    reply_markup=kb.get_sex_keyboard())

        case 'register_tenant_city' | 'register_landlord_city' as register_city:
            if 'tenant' in register_city:
                await RegisterTenantStates.CITY_STATE.set()
            elif 'landlord' in register_city:
                await RegisterLandlordStates.CITY_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите город:')

        case 'register_tenant_qualities':
            await RegisterTenantStates.QUALITIES_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите персональные качества:')

        case 'register_tenant_age' | 'register_landlord_age' as register_age:
            if 'tenant' in register_age:
                await RegisterTenantStates.AGE_STATE.set()
            elif 'landlord' in register_age:
                await RegisterLandlordStates.AGE_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите возраст:')

        case 'register_tenant_solvency':
            await RegisterTenantStates.SOLVENCY_STATE.set()
            await SayNoToHostelBot.bot.send_message(
                callback_query.from_user.id, 'Укажите, являетесь ли вы платежеспособным:',
                reply_markup=kb.get_solvency_keyboard()
            )

        case 'register_landlord_phone':
            await RegisterLandlordStates.PHONE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите номер телефона:')

        case 'register_tenant_finish' | 'register_landlord_finish' as register_finish:
            async with state.proxy() as data:
                if 'tenant' in register_finish:
                    fields = ['name', 'sex', 'city', 'age']
                    ru_fields = ['Имя', 'Пол', 'Город', 'Возраст']
                elif 'landlord' in register_finish:
                    fields = ['name', 'city', 'age', 'phone']
                    ru_fields = ['Имя', 'Город', 'Возраст', 'Телефон']
                else:
                    raise ValueError('Invalid param to callback')

                blank = [ru_fields[fields.index(field)] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    if 'tenant' in register_finish:
                        await register_form(callback_query.from_user.id, kb.get_register_tenant_keyboard())
                    elif 'landlord' in register_finish:
                        await register_form(callback_query.from_user.id, kb.get_register_landlord_keyboard())
                    else:
                        raise ValueError('Invalid param to callback')
                else:
                    register_data = [data[field] for field in fields]
                    if 'tenant' in register_finish:
                        qualities = data['qualities'] if 'qualities' in data else ''
                        solvency = data['solvency'] if 'solvency' in data else 'null'
                        user = SayNoToHostelBot.controller.register_tenant(
                            callback_query.from_user.id, *register_data[:-1], qualities, register_data[-1], solvency)
                    elif 'landlord' in register_finish:
                        user = SayNoToHostelBot.controller.register_landlord(callback_query.from_user.id,
                                                                             *register_data,
                                                                             callback_query.from_user.username)
                    else:
                        raise ValueError('Invalid param to callback')

                    if user:
                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Регистрация успешно завершена')
                        SayNoToHostelBot.check_tenant(callback_query.from_user.id)
                        SayNoToHostelBot.check_landlord(callback_query.from_user.id)
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время регистрации произошла ошибка')

        case 'register_tenant_exit' | 'register_landlord_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Вы прервали регистрацию')

        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


async def input_register_str(message: types.Message, state: FSMContext, field: str, user: EntityTypes):
    async with state.proxy() as data:
        data[field] = message.text

    if user == EntityTypes.TENANT:
        await RegisterTenantStates.START_STATE.set()
        await register_form(message.from_user.id, kb.get_register_tenant_keyboard())
    elif user == EntityTypes.LANDLORD:
        await RegisterLandlordStates.START_STATE.set()
        await register_form(message.from_user.id, kb.get_register_landlord_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(state=[RegisterTenantStates.NAME_STATE, RegisterLandlordStates.NAME_STATE])
async def input_name(message: types.Message, state: FSMContext):
    if await state.get_state() == RegisterTenantStates.NAME_STATE.state:
        await input_register_str(message, state, 'name', EntityTypes.TENANT)
    elif await state.get_state() == RegisterLandlordStates.NAME_STATE.state:
        await input_register_str(message, state, 'name', EntityTypes.LANDLORD)


@SayNoToHostelBot.dispatcher.message_handler(state=[RegisterTenantStates.CITY_STATE, RegisterLandlordStates.CITY_STATE])
async def input_city(message: types.Message, state: FSMContext):
    if await state.get_state() == RegisterTenantStates.CITY_STATE.state:
        await input_register_str(message, state, 'city', EntityTypes.TENANT)
    elif await state.get_state() == RegisterLandlordStates.CITY_STATE.state:
        await input_register_str(message, state, 'city', EntityTypes.LANDLORD)


@SayNoToHostelBot.dispatcher.message_handler(state=RegisterTenantStates.QUALITIES_STATE)
async def input_qualities(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'qualities', EntityTypes.TENANT)


@SayNoToHostelBot.dispatcher.message_handler(state=RegisterLandlordStates.PHONE_STATE)
async def input_phone(message: types.Message, state: FSMContext):
    if len(message.text) <= 10:
        await SayNoToHostelBot.bot.send_message(message.from_user.id,
                                                'Телефон должен быть больше, чем 10-значной последовательностью цифр')
        await RegisterLandlordStates.START_STATE.set()
        await register_form(message.from_user.id, kb.get_register_landlord_keyboard())
    else:
        await input_register_str(message, state, 'phone', EntityTypes.LANDLORD)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=RegisterTenantStates.SEX_STATE, text_contains='sex')
async def input_sex(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'sex_male' | 'sex_female':
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['sex'] = 'M' if callback_query.data == 'sex_male' else 'F'
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id, kb.get_register_tenant_keyboard())
        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


@SayNoToHostelBot.dispatcher.message_handler(state=[RegisterTenantStates.AGE_STATE, RegisterLandlordStates.AGE_STATE])
async def input_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        assert 14 <= age <= 100
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Возраст должен являться целым числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Возраст не может быть меньше 14 и больше 100')
    else:
        async with state.proxy() as data:
            data['age'] = age
    finally:
        if await state.get_state() == RegisterTenantStates.AGE_STATE.state:
            await RegisterTenantStates.START_STATE.set()
            await register_form(message.from_user.id, kb.get_register_tenant_keyboard())
        elif await state.get_state() == RegisterLandlordStates.AGE_STATE.state:
            await RegisterLandlordStates.START_STATE.set()
            await register_form(message.from_user.id, kb.get_register_landlord_keyboard())


@SayNoToHostelBot.dispatcher.callback_query_handler(state=RegisterTenantStates.SOLVENCY_STATE, text_contains='solvency')
async def input_solvency(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'solvency_yes' | 'solvency_no':
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['solvency'] = True if callback_query.data == 'solvency_yes' else False
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id, kb.get_register_tenant_keyboard())
        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


@SayNoToHostelBot.dispatcher.message_handler(commands='show_flats')
async def show_flats(message: types.Message):
    flats, flat_photos = SayNoToHostelBot.controller.get_flats()
    for flat, photos in zip(flats, flat_photos):
        if photos[:-1]:
            media = types.MediaGroup()
            for photo in photos[:-1]:
                media.attach_photo(types.InputFile(photo))
            await SayNoToHostelBot.bot.send_media_group(message.chat.id, media=media)

        owner = SayNoToHostelBot.controller.get_landlord(flat.owner_id)
        username = owner.username
        info = f'Владелец: {owner.full_name}'
        if username:
            info += f' (@{username})'
        info += (f'\nТелефон: {owner.phone}\nЦена: {flat.price} ₽\nПлощадь: {flat.square} м²\nАдрес: {flat.address}'
                 f'\nБлижайшее метро: {flat.metro}\nЭтаж: {flat.floor}/{flat.max_floor}')

        if photos[-1:]:
            await SayNoToHostelBot.bot.send_photo(message.chat.id, types.InputFile(photos[-1]), caption=info)
            await SayNoToHostelBot.bot.send_message(message.chat.id, f'Описание: {flat.description}')
        else:
            info += f'\nОписание: {flat.description}'
            await SayNoToHostelBot.bot.send_message(message.from_user.id, info)


async def add_flat_form(user_id: int):
    await SayNoToHostelBot.bot.send_message(user_id, 'Введите данные о квартире:',
                                            reply_markup=kb.get_add_flat_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='add_flat')
async def add_flat(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.LANDLORD:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы '
                                                                      'как арендодатель')
    else:
        async with state.proxy() as data:
            data['photo'] = []
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=AddFlatStates.START_STATE, text_contains='add_flat')
async def register_tenant(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'add_flat_price':
            await AddFlatStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите цену:')

        case 'add_flat_square':
            await AddFlatStates.SQUARE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите площадь:')

        case 'add_flat_address':
            await AddFlatStates.ADDRESS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите адрес:')

        case 'add_flat_floor':
            await AddFlatStates.FLOOR_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                    'Введите через пробел этаж и последний этаж в доме:')

        case 'add_flat_metro':
            await AddFlatStates.METRO_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите ближайшее метро:')

        case 'add_flat_description':
            await AddFlatStates.DESCRIPTION_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите описание:')

        case 'add_flat_photo':
            await AddFlatStates.PHOTO_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Отправьте фотки квартиры, '
                                                                                 'по окончании введите stop')

        case 'add_flat_finish':
            async with state.proxy() as data:
                fields = ['price', 'square', 'address']
                ru_fields = ['Цена', 'Площадь', 'Адрес']
                blank = [ru_fields[fields.index(field)] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    await add_flat_form(callback_query.from_user.id)
                else:
                    owner_id = callback_query.from_user.id
                    flat_data = [data[field] for field in fields]
                    metro = data['metro'] if 'metro' in data else ''
                    floor = data['floor'] if 'floor' in data else 0
                    max_floor = data['max_floor'] if 'max_floor' in data else 0
                    description = data['description'] if 'description' in data else ''
                    flat = SayNoToHostelBot.controller.add_flat(owner_id, *flat_data, metro, floor,
                                                                max_floor, description)
                    if flat:
                        for photo in data['photo']:
                            get_photo = SayNoToHostelBot.controller.add_photo(flat.flat_id, photo)
                            if not get_photo:
                                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                        'Во время добавления фото произошла ошибка')
                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Квартира успешно добавлена')
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время добавления квартиры произошла ошибка')
        case 'add_flat_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Вы прервали добавление')

        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


async def input_add_flat_str(message: types.Message, state: FSMContext, field: str):
    async with state.proxy() as data:
        data[field] = message.text

    await AddFlatStates.START_STATE.set()
    await add_flat_form(message.from_user.id)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.ADDRESS_STATE)
async def input_address(message: types.Message, state: FSMContext):
    await input_add_flat_str(message, state, 'address')


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.METRO_STATE)
async def input_metro(message: types.Message, state: FSMContext):
    await input_add_flat_str(message, state, 'metro')


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.DESCRIPTION_STATE)
async def input_description(message: types.Message, state: FSMContext):
    await input_add_flat_str(message, state, 'description')


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.PRICE_STATE)
async def input_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        assert price > 0
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Цена должна быть целым числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Цена не может отрицательной')
    else:
        async with state.proxy() as data:
            data['price'] = price
    finally:
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.SQUARE_STATE)
async def input_square(message: types.Message, state: FSMContext):
    try:
        square = float(message.text)
        assert square > 0
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Площадь должна быть числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Площадь не может отрицательной')
    else:
        async with state.proxy() as data:
            data['square'] = square
    finally:
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.FLOOR_STATE)
async def input_floor(message: types.Message, state: FSMContext):
    try:
        floor, max_floor = map(int, message.text.split())
        assert 0 < floor <= max_floor
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Должно быть введено два числа через пробел')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Два числа должны быть положительными '
                                                                      '(при этом первое не больше второго)')
    else:
        async with state.proxy() as data:
            data['floor'] = floor
            data['max_floor'] = max_floor
    finally:
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.PHOTO_STATE, content_types='photo')
async def input_photo(message: types.Message, state: FSMContext):
    photo_name = os.path.join(IMG_PATH, f'{message.photo[-1].file_unique_id}.jpg')
    await message.photo[-1].download(destination_file=photo_name)
    async with state.proxy() as data:
        data['photo'].append(photo_name)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.PHOTO_STATE)
async def input_photo(message: types.Message):
    if message.text == 'stop':
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id)
    else:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы ввели что-то неверное, '
                                                                      'для окончания напишите stop')


@SayNoToHostelBot.dispatcher.message_handler()
async def last_handler(message: types.Message):
    await SayNoToHostelBot.bot.send_message(message.from_user.id,
                                            'Вы ввели что-то неверное, для получения информации введите /help')

from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging
import os
from typing import Type
import src.bot.config as cfg
from src.bot.config import API_TOKEN, IMG_PATH, EntityType as EType
from src.bot.message import MESSAGE_START, MESSAGE_HELP
from src.bot.states import (
    RegisterTenantStates, RegisterLandlordStates, AddFlatStates, ShowFlatsStates, GetLandlordInfoStates,
    AddNeighborhoodStates, ShowNeighborhoodsStates, AddGoodsStates
)
from src.database.config import RolesDB
from src.database.database import BaseDatabase
from src.controller.guest import GuestController
from src.controller.tenant import TenantController
from src.controller.landlord import LandlordController
from src.model.flat import Flat
from src.model.landlord import Landlord
from src.model.neighborhood import Neighborhood
from src.model.goods import Goods
from src.model.tenant import Tenant
import src.bot.keyboard as kb


class SayNoToHostelBot:
    bot = Bot(token=API_TOKEN)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())
    database: BaseDatabase
    controller: GuestController | TenantController | LandlordController
    role: RolesDB

    controllers_dict = {
        RolesDB.GUEST: GuestController,
        RolesDB.TENANT: TenantController,
        RolesDB.LANDLORD: LandlordController
    }

    @classmethod
    def init_db(cls, database: BaseDatabase):
        assert issubclass(type(database), BaseDatabase)
        cls.database = database

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

    @classmethod
    def close_db(cls):
        cls.database.disconnect_db()


@SayNoToHostelBot.dispatcher.message_handler(commands='start')
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    logging.info('Starting bot')
    await SayNoToHostelBot.bot.send_message(user_id, MESSAGE_START)


@SayNoToHostelBot.dispatcher.message_handler(commands='help')
async def send_help(message: types.Message):
    await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)


async def get_info_from_state(state: FSMContext, fields: dict[str, str]) -> str:
    if state:
        async with state.proxy() as data:
            state_data = data
    else:
        state_data = {}

    info = ''
    for field in fields:
        info += f'{fields[field]}: '
        if state_data and field in state_data:
            info += str(state_data[field])
        info += '\n'

    return info.strip()


# ==============================================
# Register user
# ==============================================

async def register_form(user_id: int, user_type: EType, state: FSMContext = None):
    if user_type == EType.TENANT:
        fields = cfg.ALL_TENANT_FIELDS
        keyboard = kb.get_register_tenant_keyboard()
    elif user_type == EType.LANDLORD:
        fields = cfg.ALL_LANDLORD_FIELDS
        keyboard = kb.get_register_landlord_keyboard()
    else:
        raise ValueError('Invalid type of user')

    info = await get_info_from_state(state, fields)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=keyboard)


@SayNoToHostelBot.dispatcher.message_handler(commands=['register_tenant', 'register_landlord'])
async def send_register(message: types.Message):
    user_id = message.from_user.id
    if message.text.endswith('tenant'):
        if SayNoToHostelBot.check_tenant(user_id):
            await SayNoToHostelBot.bot.send_message(user_id, 'Вы вошли как арендатор')
            await SayNoToHostelBot.bot.send_message(user_id, MESSAGE_HELP)
        else:
            await RegisterTenantStates.START_STATE.set()
            await register_form(user_id, EType.TENANT)
    elif message.text.endswith('landlord'):
        if SayNoToHostelBot.check_landlord(user_id):
            await SayNoToHostelBot.bot.send_message(user_id, 'Вы вошли как арендодатель')
            await SayNoToHostelBot.bot.send_message(user_id, MESSAGE_HELP)
        else:
            await RegisterLandlordStates.START_STATE.set()
            await register_form(user_id, EType.LANDLORD)


@SayNoToHostelBot.dispatcher.callback_query_handler(
    state=[RegisterTenantStates.START_STATE, RegisterLandlordStates.START_STATE], text_contains='register')
async def register_tenant(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'register_tenant_name' | 'register_landlord_name' as register_name:
            if 'tenant' in register_name:
                await RegisterTenantStates.NAME_STATE.set()
            elif 'landlord' in register_name:
                await RegisterLandlordStates.NAME_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите полное имя')

        case 'register_tenant_sex':
            await RegisterTenantStates.SEX_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите пол',
                                                    reply_markup=kb.get_sex_keyboard())

        case 'register_tenant_city' | 'register_landlord_city' as register_city:
            if 'tenant' in register_city:
                await RegisterTenantStates.CITY_STATE.set()
            elif 'landlord' in register_city:
                await RegisterLandlordStates.CITY_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите город')

        case 'register_tenant_qualities':
            await RegisterTenantStates.QUALITIES_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите персональные качества')

        case 'register_tenant_age' | 'register_landlord_age' as register_age:
            if 'tenant' in register_age:
                await RegisterTenantStates.AGE_STATE.set()
            elif 'landlord' in register_age:
                await RegisterLandlordStates.AGE_STATE.set()
            else:
                raise ValueError('Invalid param to callback')
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите возраст')

        case 'register_tenant_solvency':
            await RegisterTenantStates.SOLVENCY_STATE.set()
            await SayNoToHostelBot.bot.send_message(
                callback_query.from_user.id, 'Укажите, являетесь ли вы платежеспособным',
                reply_markup=kb.get_solvency_keyboard()
            )

        case 'register_landlord_phone':
            await RegisterLandlordStates.PHONE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите номер телефона')

        case 'register_tenant_finish' | 'register_landlord_finish' as register_finish:
            async with state.proxy() as data:
                if 'tenant' in register_finish:
                    fields = cfg.TENANT_FIELDS
                elif 'landlord' in register_finish:
                    fields = cfg.LANDLORD_FIELDS
                    data['rating'] = 0.0
                else:
                    raise ValueError('Invalid param to callback')

                blank = [fields[field] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    if 'tenant' in register_finish:
                        await register_form(callback_query.from_user.id, EType.TENANT, state)
                    elif 'landlord' in register_finish:
                        await register_form(callback_query.from_user.id, EType.LANDLORD, state)
                    else:
                        raise ValueError('Invalid param to callback')
                else:
                    register_data = [callback_query.from_user.id] + [data[field] for field in fields]
                    if 'tenant' in register_finish:
                        qualities = data['qualities'] if 'qualities' in data else ''
                        solvency = data['solvency'] if 'solvency' in data else 'null'
                        register_data.insert(-1, qualities)
                        tenant = Tenant(*register_data, solvency, callback_query.from_user.username)
                        user = SayNoToHostelBot.controller.register_tenant(tenant)
                    elif 'landlord' in register_finish:
                        landlord = Landlord(*register_data, callback_query.from_user.username)
                        user = SayNoToHostelBot.controller.register_landlord(landlord)
                    else:
                        raise ValueError('Invalid param to callback')

                    if user:
                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Регистрация успешно завершена')
                        if 'tenant' in register_finish:
                            SayNoToHostelBot.check_tenant(callback_query.from_user.id)
                        elif 'landlord' in register_finish:
                            SayNoToHostelBot.check_landlord(callback_query.from_user.id)
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время регистрации произошла ошибка')

                    await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)

        case 'register_tenant_exit' | 'register_landlord_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_register_str(message: types.Message, state: FSMContext, field: str, user_type: EType):
    async with state.proxy() as data:
        data[field] = message.text

    if user_type == EType.TENANT:
        await RegisterTenantStates.START_STATE.set()
    elif user_type == EType.LANDLORD:
        await RegisterLandlordStates.START_STATE.set()

    await register_form(message.from_user.id, user_type, state)


@SayNoToHostelBot.dispatcher.message_handler(state=[RegisterTenantStates.NAME_STATE, RegisterLandlordStates.NAME_STATE])
async def input_name(message: types.Message, state: FSMContext):
    if await state.get_state() == RegisterTenantStates.NAME_STATE.state:
        await input_register_str(message, state, 'name', EType.TENANT)
    elif await state.get_state() == RegisterLandlordStates.NAME_STATE.state:
        await input_register_str(message, state, 'name', EType.LANDLORD)


@SayNoToHostelBot.dispatcher.message_handler(state=[RegisterTenantStates.CITY_STATE, RegisterLandlordStates.CITY_STATE])
async def input_city(message: types.Message, state: FSMContext):
    if await state.get_state() == RegisterTenantStates.CITY_STATE.state:
        await input_register_str(message, state, 'city', EType.TENANT)
    elif await state.get_state() == RegisterLandlordStates.CITY_STATE.state:
        await input_register_str(message, state, 'city', EType.LANDLORD)


@SayNoToHostelBot.dispatcher.message_handler(state=RegisterTenantStates.QUALITIES_STATE)
async def input_qualities(message: types.Message, state: FSMContext):
    await input_register_str(message, state, 'qualities', EType.TENANT)


@SayNoToHostelBot.dispatcher.message_handler(state=RegisterLandlordStates.PHONE_STATE)
async def input_phone(message: types.Message, state: FSMContext):
    if len(message.text) <= 10:
        await SayNoToHostelBot.bot.send_message(message.from_user.id,
                                                'Телефон должен быть больше, чем 10-значной последовательностью цифр')
        await RegisterLandlordStates.START_STATE.set()
        await register_form(message.from_user.id, EType.LANDLORD, state)
    else:
        await input_register_str(message, state, 'phone', EType.LANDLORD)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=RegisterTenantStates.SEX_STATE, text_contains='sex')
async def input_sex(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'sex_male' | 'sex_female' as sex:
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['sex'] = 'M' if sex == 'sex_male' else 'F'
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id, EType.TENANT, state)
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
            await register_form(message.from_user.id, EType.TENANT, state)
        elif await state.get_state() == RegisterLandlordStates.AGE_STATE.state:
            await RegisterLandlordStates.START_STATE.set()
            await register_form(message.from_user.id, EType.LANDLORD, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=RegisterTenantStates.SOLVENCY_STATE, text_contains='solvency')
async def input_solvency(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'solvency_yes' | 'solvency_no':
            await RegisterTenantStates.START_STATE.set()
            async with state.proxy() as data:
                data['solvency'] = True if callback_query.data == 'solvency_yes' else False
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
            await register_form(callback_query.from_user.id, EType.TENANT, state)
        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


# ==============================================
# Show flats
# ==============================================


async def show_flat(chat_id: int, flat: Flat, photos: list[str], paginate: bool = True) -> list[types.Message]:
    flat_messages: list[types.Message] = []

    if photos[:-1]:
        media = types.MediaGroup()
        for photo in photos[:-1]:
            media.attach_photo(types.InputFile(photo))
        flat_messages += await SayNoToHostelBot.bot.send_media_group(chat_id, media=media)

    owner = SayNoToHostelBot.controller.get_landlord(flat.owner_id)
    username = owner.username
    info = f'Владелец: {owner.full_name}'
    if username:
        info += f' (@{username})'
    info += (f'\nТелефон: {owner.phone}\nЦена: {flat.price} ₽\nКомнаты: {flat.rooms}\nПлощадь: {flat.square} м²\n'
             f'Адрес: {flat.address}\nБлижайшее метро: {flat.metro}\nЭтаж: {flat.floor}/{flat.max_floor}')

    if photos[-1:]:
        flat_messages.append(await SayNoToHostelBot.bot.send_photo(chat_id, types.InputFile(photos[-1]), caption=info))
        flat_messages.append(await SayNoToHostelBot.bot.send_message(chat_id, f'Описание: {flat.description}'))
    else:
        info += f'\nОписание: {flat.description}'
        flat_messages.append(await SayNoToHostelBot.bot.send_message(chat_id, info))

    if paginate:
        await flat_messages[-1].edit_reply_markup(reply_markup=kb.get_pagination_keyboard())
    return flat_messages


async def show_flat_form(user_id: int, state: FSMContext):
    info = await get_info_from_state(state, cfg.FILTER_FLAT_FIELDS)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=kb.get_flats_filter_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='show_flats_filters')
async def show_flats_filters_start(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.TENANT and SayNoToHostelBot.role != RolesDB.LANDLORD:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы')
    else:
        async with state.proxy() as data:
            data['metro'] = []
        await ShowFlatsStates.START_STATE.set()
        await show_flat_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=ShowFlatsStates.START_STATE, text_contains='show_flats')
async def add_flat_filter(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'show_flats_price':
            await ShowFlatsStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите через пробел минимальную '
                                                                                 'и максимальную цену')

        case 'show_flats_rooms':
            await ShowFlatsStates.ROOMS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите через пробел минимальное '
                                                                                 'и максимальное количество комнат')

        case 'show_flats_square':
            await ShowFlatsStates.SQUARE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите через пробел минимальную '
                                                                                 'и максимальную площадь')

        case 'show_flats_metro':
            await ShowFlatsStates.METRO_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите ближайшие станции метро '
                                                                                 'через запятую')

        case 'show_flats_finish':
            async with state.proxy() as data:
                price = (tuple(data['price'].split(' - '))) if 'price' in data else ()
                rooms = (tuple(data['rooms'].split(' - '))) if 'rooms' in data else ()
                square = (tuple(data['square'].split(' - '))) if 'square' in data else ()
                metro = data['metro'] if 'metro' in data else []

                flats, flat_photos = SayNoToHostelBot.controller.get_flats_filters(price, rooms, square, metro)

            if flats:
                await state.finish()

                flat, photos = flats[0], flat_photos[0]
                flat_messages = await show_flat(callback_query.from_user.id, flat, photos)

                if flat_messages:
                    async with state.proxy() as data:
                        data['message'] = flat_messages
                        data['flats'] = (flats, flat_photos)
                        data['cur_flat'] = 0
                    await ShowFlatsStates.PAGINATION_STATE.set()
            else:
                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                        'По данным параметрам квартир не найдено')
                await show_flat_form(callback_query.from_user.id, state)

        case 'show_flats_subscribe':
            async with state.proxy() as data:
                price = (tuple(data['price'].split(' - '))) if 'price' in data else ()
                rooms = (tuple(data['rooms'].split(' - '))) if 'rooms' in data else ()
                square = (tuple(data['square'].split(' - '))) if 'square' in data else ()
                metro = data['metro'] if 'metro' in data else []

                SayNoToHostelBot.controller.unsubscribe_flat(callback_query.from_user.id)
                if SayNoToHostelBot.controller.subscribe_flat(callback_query.from_user.id, price, rooms, square, metro):
                    await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                            'Вы успешно подписались на квартиры с данными параметрами')
                else:
                    await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                            'Во время подписки произошла ошибка')
                await show_flat_form(callback_query.from_user.id, state)

        case 'show_flats_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_show_flat_range(message: types.Message, state: FSMContext, field: str,
                                nums_type: Type[int] | Type[float]):
    try:
        if nums_type == Type[float]:
            min_field, max_field = map(float, message.text.split())
        else:
            min_field, max_field = map(int, message.text.split())
        assert 0 < min_field <= max_field
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Должно быть введено два числа через пробел')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Два числа должны быть положительными '
                                                                      '(при этом первое не больше второго)')
    else:
        async with state.proxy() as data:
            data[field] = f'{min_field} - {max_field}'
    finally:
        await ShowFlatsStates.START_STATE.set()
        await show_flat_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(state=ShowFlatsStates.PRICE_STATE)
async def input_price(message: types.Message, state: FSMContext):
    await input_show_flat_range(message, state, 'price', Type[int])


@SayNoToHostelBot.dispatcher.message_handler(state=ShowFlatsStates.ROOMS_STATE)
async def input_rooms(message: types.Message, state: FSMContext):
    await input_show_flat_range(message, state, 'rooms', Type[int])


@SayNoToHostelBot.dispatcher.message_handler(state=ShowFlatsStates.SQUARE_STATE)
async def input_square(message: types.Message, state: FSMContext):
    await input_show_flat_range(message, state, 'square', Type[float])


@SayNoToHostelBot.dispatcher.message_handler(state=ShowFlatsStates.METRO_STATE)
async def input_metro(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['metro'] = message.text.split(',')

    await ShowFlatsStates.START_STATE.set()
    await show_flat_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(commands='show_flats')
async def show_flats(message: types.Message, state: FSMContext):
    flats, flat_photos = SayNoToHostelBot.controller.get_flats()
    if not flats:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Квартир не найдено')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
        return

    flat, photos = flats[0], flat_photos[0]
    flat_messages = await show_flat(message.chat.id, flat, photos)

    if flat_messages:
        async with state.proxy() as data:
            data['message'] = flat_messages
            data['flats'] = (flats, flat_photos)
            data['cur_flat'] = 0
        await ShowFlatsStates.PAGINATION_STATE.set()


@SayNoToHostelBot.dispatcher.callback_query_handler(state=ShowFlatsStates.PAGINATION_STATE, text_contains='pagination')
async def paginate_flats(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'pagination_left':
            async with state.proxy() as data:
                data['cur_flat'] -= 1 if data['cur_flat'] > 0 else 0
                cur_flat: int = data['cur_flat']
                flat_messages: list[types.Message] = data['message']
                flats, flat_photos = data['flats']

                for message in flat_messages:
                    try:
                        await message.delete()
                    except exceptions.MessageToDeleteNotFound as e:
                        logging.error(e)

                flat_messages = await show_flat(callback_query.from_user.id, flats[cur_flat], flat_photos[cur_flat])
                data['message'] = flat_messages

        case 'pagination_right':
            async with state.proxy() as data:
                flat_messages: list[types.Message] = data['message']
                flats, flat_photos = data['flats']
                data['cur_flat'] += 1 if data['cur_flat'] < len(flats) - 1 else 0
                cur_flat: int = data['cur_flat']

                for message in flat_messages:
                    try:
                        await message.delete()
                    except exceptions.MessageToDeleteNotFound as e:
                        logging.error(e)

                flat_messages = await show_flat(callback_query.from_user.id, flats[cur_flat], flat_photos[cur_flat])
                data['message'] = flat_messages

        case 'pagination_like':
            if SayNoToHostelBot.role != RolesDB.TENANT:
                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                        'Вы должны быть зарегистрированы как арендатор')
                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)
            else:
                async with state.proxy() as data:
                    tenant_id = callback_query.from_user.id
                    flats, photos = data['flats']
                    cur_flat = data['cur_flat']
                    flat, flat_photos = flats[cur_flat], photos[cur_flat]

                    if not SayNoToHostelBot.controller.check_like_flat(tenant_id, flat.id):
                        tenants = SayNoToHostelBot.controller.get_likes_flat(flat.id)
                        cur_tenant = SayNoToHostelBot.controller.get_tenant(tenant_id)
                        name = cur_tenant.full_name + f' (@{callback_query.from_user.username})'

                        for tenant in tenants:
                            await SayNoToHostelBot.bot.send_message(tenant.id,
                                                                    f'Пользователь с именем {name} оценил квартиру')
                            await show_flat(tenant.id, flat, flat_photos, False)

                        if SayNoToHostelBot.controller.like_flat(tenant_id, flat.id):
                            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                    'Вы успешно поставили отметку \'Нравится\' на '
                                                                    'данную квартиру')
                        else:
                            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                    'При добавлении отметки "Нравится" '
                                                                    'произошла ошибка')
                    else:
                        if SayNoToHostelBot.controller.unlike_flat(tenant_id, flat.id):
                            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                    'Вы успешно убрали отметку \'Нравится\' на '
                                                                    'данную квартиру')
                        else:
                            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                    'При удалении отметки "Нравится" произошла ошибка')

                    flat_messages = await show_flat(callback_query.from_user.id, flat, flat_photos)
                    data['message'] = flat_messages

        case 'pagination_cancel':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


# ==============================================
# Add flats
# ==============================================

async def add_flat_form(user_id: int, state: FSMContext):
    info = await get_info_from_state(state, cfg.ALL_FLAT_FIELDS)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=kb.get_add_flat_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='add_flat')
async def add_flat_start(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.LANDLORD:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы '
                                                                      'как арендодатель')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
    else:
        async with state.proxy() as data:
            data['photo'] = []
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=AddFlatStates.START_STATE, text_contains='add_flat')
async def add_flat(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'add_flat_price':
            await AddFlatStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите цену')

        case 'add_flat_rooms':
            await AddFlatStates.ROOMS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите количество комнат')

        case 'add_flat_square':
            await AddFlatStates.SQUARE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите площадь')

        case 'add_flat_address':
            await AddFlatStates.ADDRESS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите адрес')

        case 'add_flat_floor':
            await AddFlatStates.FLOOR_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                    'Введите через пробел этаж и последний этаж в доме')

        case 'add_flat_metro':
            await AddFlatStates.METRO_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите ближайшее метро')

        case 'add_flat_description':
            await AddFlatStates.DESCRIPTION_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите описание')

        case 'add_flat_photo':
            await AddFlatStates.PHOTO_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Отправьте фотки квартиры, '
                                                                                 'по окончании введите stop')

        case 'add_flat_finish':
            async with state.proxy() as data:
                fields = cfg.FLAT_FIELDS
                blank = [fields[field] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    await add_flat_form(callback_query.from_user.id, state)
                else:
                    owner_id = callback_query.from_user.id
                    flat_data = [data[field] for field in fields]
                    metro = data['metro'] if 'metro' in data else ''
                    floor = data['floor'] if 'floor' in data else 0
                    max_floor = data['max_floor'] if 'max_floor' in data else 0
                    description = data['description'] if 'description' in data else ''
                    new_flat = Flat(-1, owner_id, *flat_data, metro, floor, max_floor, description)
                    flat = SayNoToHostelBot.controller.add_flat(new_flat)
                    if flat:
                        photos = []
                        for photo in data['photo']:
                            new_photo = SayNoToHostelBot.controller.add_photo(flat.id, photo)
                            if not new_photo:
                                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                        'Во время добавления фото произошла ошибка')
                            else:
                                photos.append(new_photo)

                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Квартира успешно добавлена')

                        tenants = SayNoToHostelBot.controller.get_tenants_subscription(owner_id)
                        tenants += SayNoToHostelBot.controller.get_subscribed_flat_tenants(
                            flat.price, flat.rooms, flat.square, flat.metro
                        )
                        for tenant in tenants:
                            await SayNoToHostelBot.bot.send_message(tenant.id,
                                                                    'По вашим подпискам была добавлена новая квартира')
                            await show_flat(tenant.id, flat, photos, False)
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время добавления квартиры произошла ошибка')
        case 'add_flat_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_add_flat_str(message: types.Message, state: FSMContext, field: str):
    async with state.proxy() as data:
        data[field] = message.text

    await AddFlatStates.START_STATE.set()
    await add_flat_form(message.from_user.id, state)


async def input_add_flat_num(message: types.Message, state: FSMContext, field: str, num_type: Type[int] | Type[float]):
    try:
        if num_type == Type[float]:
            value = float(message.text)
        else:
            value = int(message.text)
        assert value > 0
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение должно быть числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение не может быть отрицательным')
    else:
        async with state.proxy() as data:
            data[field] = value
    finally:
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id, state)


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
    await input_add_flat_num(message, state, 'price', Type[int])


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.ROOMS_STATE)
async def input_rooms(message: types.Message, state: FSMContext):
    await input_add_flat_num(message, state, 'rooms', Type[int])


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.SQUARE_STATE)
async def input_square(message: types.Message, state: FSMContext):
    await input_add_flat_num(message, state, 'square', Type[float])


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
        await add_flat_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.PHOTO_STATE, content_types='photo')
async def input_photo(message: types.Message, state: FSMContext):
    photo_name = os.path.join(IMG_PATH, f'{message.photo[-1].file_unique_id}.jpg')
    await message.photo[-1].download(destination_file=photo_name)
    async with state.proxy() as data:
        data['photo'].append(photo_name)


@SayNoToHostelBot.dispatcher.message_handler(state=AddFlatStates.PHOTO_STATE)
async def input_photo(message: types.Message, state: FSMContext):
    if message.text.lower() == 'stop':
        await AddFlatStates.START_STATE.set()
        await add_flat_form(message.from_user.id, state)
    else:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы ввели что-то неверное, '
                                                                      'для окончания напишите stop')


# ==============================================
# Get landlord info
# ==============================================


@SayNoToHostelBot.dispatcher.message_handler(commands='get_landlord_info')
async def get_landlord_info(message: types.Message):
    if SayNoToHostelBot.role != RolesDB.TENANT:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы как арендатор')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
    else:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Введите имя арендодателя')
        await GetLandlordInfoStates.NAME_STATE.set()


@SayNoToHostelBot.dispatcher.message_handler(state=GetLandlordInfoStates.NAME_STATE)
async def input_landlord_name(message: types.Message, state: FSMContext):
    landlord = SayNoToHostelBot.controller.get_landlord(message.text)
    if not landlord:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Арендодатель с данным именем не зарегистрирован')
        await state.finish()
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
    else:
        async with state.proxy() as data:
            data.update(landlord.get_params_dict())
            data['landlord'] = landlord
            data['name'] = landlord.full_name
            data['old_rating'] = landlord.rating

        info = await get_info_from_state(state, cfg.LANDLORD_FIELDS)
        await SayNoToHostelBot.bot.send_message(message.from_user.id, info,
                                                reply_markup=kb.get_landlord_info_keyboard())
        await GetLandlordInfoStates.START_STATE.set()


@SayNoToHostelBot.dispatcher.callback_query_handler(
    state=GetLandlordInfoStates.START_STATE, text_contains='get_landlord')
async def rate_landlord(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'get_landlord_rating':
            await GetLandlordInfoStates.RATING_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                    'Введите оценку (целое число от 1 до 10)')

        case 'get_landlord_subscribe':
            async with state.proxy() as data:
                tenant_id = callback_query.from_user.id
                landlord_id = data['landlord'].id
                if not SayNoToHostelBot.controller.check_subscription_landlord(tenant_id, landlord_id):
                    if SayNoToHostelBot.controller.subscribe_landlord(tenant_id, landlord_id):
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Вы успешно подписались на арендодателя')
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время подписки на арендодателя произошла ошибка')
                else:
                    if SayNoToHostelBot.controller.unsubscribe_landlord(tenant_id, landlord_id):
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Вы успешно отписались от арендодателя')
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время отписки от арендодателя произошла ошибка')

            info = await get_info_from_state(state, cfg.LANDLORD_FIELDS)
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, info,
                                                    reply_markup=kb.get_landlord_info_keyboard())

        case 'get_landlord_cancel':
            async with state.proxy() as data:
                landlord = data['landlord']
                landlord.set_rating(data['rating'])
            SayNoToHostelBot.controller.update_landlord(landlord)
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


@SayNoToHostelBot.dispatcher.message_handler(state=GetLandlordInfoStates.RATING_STATE)
async def input_rating(message: types.Message, state: FSMContext):
    try:
        rating = int(message.text)
        assert 1 <= rating <= 10
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Должно быть введено целое число')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Число должно быть от 1 до 10')
    else:
        async with state.proxy() as data:
            data['rating'] = round((data['old_rating'] + rating) / 2, 1)
    finally:
        info = await get_info_from_state(state, cfg.LANDLORD_FIELDS)
        await SayNoToHostelBot.bot.send_message(message.from_user.id, info,
                                                reply_markup=kb.get_landlord_info_keyboard())
        await GetLandlordInfoStates.START_STATE.set()


# ==============================================
# Add neighborhood
# ==============================================

async def add_neighborhood_form(user_id: int, state: FSMContext):
    info = await get_info_from_state(state, cfg.ALL_NEIGHBORHOOD_FIELDS)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=kb.get_add_neighborhood_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='add_neighborhood')
async def add_neighborhood_start(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.TENANT:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы '
                                                                      'как арендатор')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
    else:
        async with state.proxy() as data:
            data['photo'] = []
        await AddNeighborhoodStates.START_STATE.set()
        await add_neighborhood_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(
    state=AddNeighborhoodStates.START_STATE, text_contains='add_neighborhood')
async def add_neighborhood(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'add_neighborhood_neighbors':
            await AddNeighborhoodStates.NEIGHBORS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите количество соседей')

        case 'add_neighborhood_price':
            await AddNeighborhoodStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите желаемую цену')

        case 'add_neighborhood_place':
            await AddNeighborhoodStates.PLACE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите местоположение')

        case 'add_neighborhood_sex':
            await AddNeighborhoodStates.SEX_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите желаемый пол',
                                                    reply_markup=kb.get_expanded_sex_keyboard())

        case 'add_neighborhood_preferences':
            await AddNeighborhoodStates.PREFERENCES_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите личные предпочтения')

        case 'add_neighborhood_finish':
            async with state.proxy() as data:
                fields = cfg.NEIGHBORHOOD_FIELDS
                blank = [fields[field] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    await add_neighborhood_form(callback_query.from_user.id, state)
                else:
                    place = data['place'] if 'place' in data else ''
                    preferences = data['preferences'] if 'preferences' in data else ''

                    tenant_id = callback_query.from_user.id
                    neighbor_data = [data[field] for field in fields]
                    neighbor_data.insert(-1, place)
                    new_neighborhood = Neighborhood(-1, tenant_id, *neighbor_data, preferences)
                    neighborhood = SayNoToHostelBot.controller.add_neighborhood(new_neighborhood)

                    if neighborhood:
                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Объявление о соседстве успешно добавлено')
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время добавления объявления произошла ошибка')

        case 'add_neighborhood_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_add_neighborhood_str(message: types.Message, state: FSMContext, field: str):
    async with state.proxy() as data:
        data[field] = message.text

    await AddNeighborhoodStates.START_STATE.set()
    await add_neighborhood_form(message.from_user.id, state)


async def input_add_neighborhood_int(message: types.Message, state: FSMContext, field: str):
    try:
        value = int(message.text)
        assert value > 0
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение должно быть целым числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение не может быть отрицательным')
    else:
        async with state.proxy() as data:
            data[field] = value
    finally:
        await AddNeighborhoodStates.START_STATE.set()
        await add_neighborhood_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(state=AddNeighborhoodStates.NEIGHBORS_STATE)
async def input_neighbors(message: types.Message, state: FSMContext):
    await input_add_neighborhood_int(message, state, 'neighbors')


@SayNoToHostelBot.dispatcher.message_handler(state=AddNeighborhoodStates.PRICE_STATE)
async def input_price(message: types.Message, state: FSMContext):
    await input_add_neighborhood_int(message, state, 'price')


@SayNoToHostelBot.dispatcher.message_handler(state=AddNeighborhoodStates.PLACE_STATE)
async def input_place(message: types.Message, state: FSMContext):
    await input_add_neighborhood_str(message, state, 'place')


@SayNoToHostelBot.dispatcher.callback_query_handler(
    state=[AddNeighborhoodStates.SEX_STATE, ShowNeighborhoodsStates.SEX_STATE], text_contains='expanded_sex')
async def input_sex(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'expanded_sex_male' | 'expanded_sex_female' | 'expanded_sex_no_male' as sex:
            async with state.proxy() as data:
                data['sex'] = sex.split('_')[2][0].upper()
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
            await AddNeighborhoodStates.START_STATE.set()
            await add_neighborhood_form(callback_query.from_user.id, state)
        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


@SayNoToHostelBot.dispatcher.message_handler(state=AddNeighborhoodStates.PREFERENCES_STATE)
async def input_preferences(message: types.Message, state: FSMContext):
    await input_add_neighborhood_str(message, state, 'preferences')


# ==============================================
# Show neighborhood
# ==============================================

async def show_neighborhood(chat_id: int, neighborhood: Neighborhood, paginate: bool = True) -> types.Message:
    tenant = SayNoToHostelBot.controller.get_tenant(neighborhood.tenant_id)
    username = tenant.username
    info = f'Арендатор: {tenant.full_name}'
    if username:
        info += f' (@{username})'
    info += (f'\nКоличество соседей: {neighborhood.neighbors}\nЖелаемая цена: {neighborhood.price} ₽\n'
             f'Местоположение: {neighborhood.place}\nЖелаемый пол: {neighborhood.sex}\n'
             f'Личные предпочтения: {neighborhood.preferences}')

    message = await SayNoToHostelBot.bot.send_message(chat_id, info)
    if paginate:
        await message.edit_reply_markup(reply_markup=kb.get_pagination_keyboard(True))

    return message


async def show_neighborhood_form(user_id: int, state: FSMContext):
    info = await get_info_from_state(state, cfg.FILTER_NEIGHBORHOOD_FIELDS)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=kb.get_neighborhoods_filter_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='show_neighborhoods_filters')
async def show_neighborhoods_filters_start(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.TENANT and SayNoToHostelBot.role != RolesDB.LANDLORD:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы')
    else:
        await ShowNeighborhoodsStates.START_STATE.set()
        await show_neighborhood_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=ShowNeighborhoodsStates.START_STATE,
                                                    text_contains='show_neighborhoods')
async def add_neighborhood_filter(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'show_neighborhoods_neighbors':
            await ShowNeighborhoodsStates.NEIGHBORS_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите через пробел минимальную '
                                                                                 'и максимальную количество соседей')
        case 'show_neighborhoods_price':
            await ShowNeighborhoodsStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите через пробел минимальную '
                                                                                 'и максимальную цену')

        case 'show_neighborhoods_sex':
            await ShowNeighborhoodsStates.SEX_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите желаемый пол',
                                                    reply_markup=kb.get_expanded_sex_keyboard())

        case 'show_neighborhoods_finish':
            async with state.proxy() as data:
                neighbors = (tuple(data['neighbors'].split(' - '))) if 'neighbors' in data else ()
                price = (tuple(data['price'].split(' - '))) if 'price' in data else ()
                sex = data['sex'] if 'sex' in data else ''

                neighborhoods = SayNoToHostelBot.controller.get_neighborhoods_filters(neighbors, price, sex)

            if neighborhoods:
                await state.finish()

                neighborhood_message = await show_neighborhood(callback_query.from_user.id, neighborhoods[0])
                if neighborhood_message:
                    async with state.proxy() as data:
                        data['message'] = neighborhood_message
                        data['neighborhoods'] = neighborhoods
                        data['cur_neighborhood'] = 0
                    await ShowNeighborhoodsStates.PAGINATION_STATE.set()
            else:
                await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                        'По данным параметрам объявлений не найдено')
                await show_flat_form(callback_query.from_user.id, state)

        case 'show_neighborhoods_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_show_neighborhood_range(message: types.Message, state: FSMContext, field: str):
    try:
        min_field, max_field = map(int, message.text.split())
        assert 0 < min_field <= max_field
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Должно быть введено два числа через пробел')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Два числа должны быть положительными '
                                                                      '(при этом первое не больше второго)')
    else:
        async with state.proxy() as data:
            data[field] = f'{min_field} - {max_field}'
    finally:
        await ShowNeighborhoodsStates.START_STATE.set()
        await show_neighborhood_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(state=ShowNeighborhoodsStates.NEIGHBORS_STATE)
async def input_price(message: types.Message, state: FSMContext):
    await input_show_neighborhood_range(message, state, 'neighbors')


@SayNoToHostelBot.dispatcher.message_handler(state=ShowNeighborhoodsStates.PRICE_STATE)
async def input_price(message: types.Message, state: FSMContext):
    await input_show_neighborhood_range(message, state, 'price')


@SayNoToHostelBot.dispatcher.message_handler(commands='show_neighborhoods')
async def show_neighborhoods(message: types.Message, state: FSMContext):
    neighborhoods = SayNoToHostelBot.controller.get_neighborhoods()
    if not neighborhoods:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Объявлений не найдено')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
        return

    neighborhood_message = await show_neighborhood(message.from_user.id, neighborhoods[0])
    if neighborhood_message:
        async with state.proxy() as data:
            data['message'] = neighborhood_message
            data['neighborhoods'] = neighborhoods
            data['cur_neighborhood'] = 0
        await ShowNeighborhoodsStates.PAGINATION_STATE.set()


@SayNoToHostelBot.dispatcher.callback_query_handler(state=ShowNeighborhoodsStates.PAGINATION_STATE,
                                                    text_contains='pagination')
async def paginate_neighborhoods(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'pagination_left':
            async with state.proxy() as data:
                data['cur_neighborhood'] -= 1 if data['cur_neighborhood'] > 0 else 0
                cur_neighborhood: int = data['cur_neighborhood']
                neighborhood_message: types.Message = data['message']
                neighborhoods: list[Neighborhood] = data['neighborhoods']

                try:
                    await neighborhood_message.delete()
                except exceptions.MessageToDeleteNotFound as e:
                    logging.error(e)

                neighborhood_message = await show_neighborhood(callback_query.from_user.id,
                                                               neighborhoods[cur_neighborhood])
                data['message'] = neighborhood_message

        case 'pagination_right':
            async with state.proxy() as data:
                neighborhood_message: types.Message = data['message']
                neighborhoods: list[Neighborhood] = data['neighborhoods']
                data['cur_neighborhood'] += 1 if data['cur_neighborhood'] < len(neighborhoods) - 1 else 0
                cur_neighborhood: int = data['cur_neighborhood']

                try:
                    await neighborhood_message.delete()
                except exceptions.MessageToDeleteNotFound as e:
                    logging.error(e)

                neighborhood_message = await show_neighborhood(callback_query.from_user.id,
                                                               neighborhoods[cur_neighborhood])
                data['message'] = neighborhood_message

        case 'pagination_cancel':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)

        case _:
            await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)


# ==============================================
# Add goods
# ==============================================

async def add_goods_form(user_id: int, state: FSMContext):
    info = await get_info_from_state(state, cfg.ALL_GOODS_FIELDS)
    await SayNoToHostelBot.bot.send_message(user_id, info, reply_markup=kb.get_add_goods_keyboard())


@SayNoToHostelBot.dispatcher.message_handler(commands='add_goods')
async def add_goods_start(message: types.Message, state: FSMContext):
    if SayNoToHostelBot.role != RolesDB.TENANT:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Вы должны быть зарегистрированы '
                                                                      'как арендатор')
        await SayNoToHostelBot.bot.send_message(message.from_user.id, MESSAGE_HELP)
    else:
        async with state.proxy() as data:
            data['photo'] = []
        await AddGoodsStates.START_STATE.set()
        await add_goods_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=AddGoodsStates.START_STATE, text_contains='add_goods')
async def add_goods(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)
    match callback_query.data:
        case 'add_goods_name':
            await AddGoodsStates.NAME_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите название')

        case 'add_goods_price':
            await AddGoodsStates.PRICE_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Введите цену')

        case 'add_goods_condition':
            await AddGoodsStates.CONDITION_STATE.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите состояние',
                                                    reply_markup=kb.get_condition_keyboard())

        case 'add_goods_bargain':
            await AddGoodsStates.BARGAIN.set()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, 'Укажите, возможен ли торг',
                                                    reply_markup=kb.get_bargain_keyboard())

        case 'add_goods_finish':
            async with state.proxy() as data:
                fields = cfg.GOODS_FIELDS
                blank = [fields[field] for field in fields
                         if field not in data]
                if blank:
                    await SayNoToHostelBot.bot.send_message(
                        callback_query.from_user.id, 'Обязательными полями для ввода являются: ' + ', '.join(blank))
                    await add_goods_form(callback_query.from_user.id, state)
                else:
                    bargain = data['bargain'] if 'bargain' in data else 'null'

                    tenant_id = callback_query.from_user.id
                    goods_data = [data[field] for field in fields]
                    new_goods = Goods(-1, tenant_id, *goods_data, bargain)
                    goods = SayNoToHostelBot.controller.add_goods(new_goods)

                    if goods:
                        await state.finish()
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Объявление успешно добавлено')
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)
                    else:
                        await SayNoToHostelBot.bot.send_message(callback_query.from_user.id,
                                                                'Во время добавления объявления произошла ошибка')

        case 'add_goods_exit':
            await state.finish()
            await SayNoToHostelBot.bot.send_message(callback_query.from_user.id, MESSAGE_HELP)


async def input_add_goods_str(message: types.Message, state: FSMContext, field: str):
    async with state.proxy() as data:
        data[field] = message.text

    await AddGoodsStates.START_STATE.set()
    await add_goods_form(message.from_user.id, state)


async def input_add_goods_int(message: types.Message, state: FSMContext, field: str):
    try:
        value = int(message.text)
        assert value > 0
    except ValueError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение должно быть целым числом')
    except AssertionError:
        await SayNoToHostelBot.bot.send_message(message.from_user.id, 'Значение не может быть отрицательным')
    else:
        async with state.proxy() as data:
            data[field] = value
    finally:
        await AddGoodsStates.START_STATE.set()
        await add_goods_form(message.from_user.id, state)


@SayNoToHostelBot.dispatcher.message_handler(state=AddGoodsStates.NAME_STATE)
async def input_name(message: types.Message, state: FSMContext):
    await input_add_goods_str(message, state, 'name')


@SayNoToHostelBot.dispatcher.message_handler(state=AddGoodsStates.PRICE_STATE)
async def input_price(message: types.Message, state: FSMContext):
    await input_add_goods_int(message, state, 'price')


@SayNoToHostelBot.dispatcher.callback_query_handler(state=AddGoodsStates.CONDITION_STATE, text_contains='condition')
async def input_condition(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['condition'] = callback_query.data.split('_')[1][0].upper()
    await AddGoodsStates.START_STATE.set()
    await add_goods_form(callback_query.from_user.id, state)


@SayNoToHostelBot.dispatcher.callback_query_handler(state=AddGoodsStates.BARGAIN, text_contains='bargain')
async def input_bargain(callback_query: types.CallbackQuery, state: FSMContext):
    await SayNoToHostelBot.bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:
        data['bargain'] = True if callback_query.data == 'bargain_yes' else False
    await AddGoodsStates.START_STATE.set()
    await add_goods_form(callback_query.from_user.id, state)


# ==============================================
# Last handler
# ==============================================

@SayNoToHostelBot.dispatcher.message_handler()
async def last_handler(message: types.Message):
    await SayNoToHostelBot.bot.send_message(message.from_user.id,
                                            'Вы ввели что-то неверное, для получения информации введите /help')

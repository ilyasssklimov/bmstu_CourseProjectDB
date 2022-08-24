from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_register_tenant_keyboard():
    register_tenant_keyboard = InlineKeyboardMarkup()
    name_btn = InlineKeyboardButton('Полное имя', callback_data='register_tenant_name')
    sex_btn = InlineKeyboardButton('Пол', callback_data='register_tenant_sex')
    city_btn = InlineKeyboardButton('Город', callback_data='register_tenant_city')
    qualities_btn = InlineKeyboardButton('Персональные качества', callback_data='register_tenant_qualities')
    age_btn = InlineKeyboardButton('Возраст', callback_data='register_tenant_age')
    solvency_btn = InlineKeyboardButton('Платежеспособность', callback_data='register_tenant_solvency')
    finish_btn = InlineKeyboardButton('Завершить регистрацию', callback_data='register_tenant_finish')
    exit_btn = InlineKeyboardButton('Прервать регистрацию', callback_data='register_tenant_exit')

    register_tenant_keyboard.row(name_btn, age_btn)
    register_tenant_keyboard.row(sex_btn, city_btn)
    register_tenant_keyboard.add(qualities_btn)
    register_tenant_keyboard.add(solvency_btn)
    register_tenant_keyboard.add(finish_btn)
    register_tenant_keyboard.add(exit_btn)

    return register_tenant_keyboard


def get_sex_keyboard():
    sex_keyboard = InlineKeyboardMarkup()
    male = InlineKeyboardButton('Мужской', callback_data='sex_male')
    female = InlineKeyboardButton('Женский', callback_data='sex_female')
    sex_keyboard.row(male, female)

    return sex_keyboard


def get_solvency_keyboard():
    solvency_keyboard = InlineKeyboardMarkup()
    yes = InlineKeyboardButton('Да', callback_data='solvency_yes')
    no = InlineKeyboardButton('Нет', callback_data='solvency_no')
    solvency_keyboard.row(yes, no)

    return solvency_keyboard


def get_register_landlord_keyboard():
    register_landlord_keyboard = InlineKeyboardMarkup()
    name_btn = InlineKeyboardButton('Полное имя', callback_data='register_landlord_name')
    city_btn = InlineKeyboardButton('Город', callback_data='register_landlord_city')
    age_btn = InlineKeyboardButton('Возраст', callback_data='register_landlord_age')
    number_btn = InlineKeyboardButton('Телефон', callback_data='register_landlord_phone')
    finish_btn = InlineKeyboardButton('Завершить регистрацию', callback_data='register_landlord_finish')
    exit_btn = InlineKeyboardButton('Прервать регистрацию', callback_data='register_landlord_exit')

    register_landlord_keyboard.row(name_btn, age_btn)
    register_landlord_keyboard.row(city_btn, number_btn)
    register_landlord_keyboard.add(finish_btn)
    register_landlord_keyboard.add(exit_btn)

    return register_landlord_keyboard


def get_add_flat_keyboard():
    add_flat_keyboard = InlineKeyboardMarkup()
    price_btn = InlineKeyboardButton('Цена', callback_data='add_flat_price')
    rooms_btn = InlineKeyboardButton('Комнаты', callback_data='add_flat_rooms')
    square_btn = InlineKeyboardButton('Площадь', callback_data='add_flat_square')
    address_btn = InlineKeyboardButton('Адрес', callback_data='add_flat_address')
    floor_btn = InlineKeyboardButton('Этаж', callback_data='add_flat_floor')
    metro_btn = InlineKeyboardButton('Ближайшее метро', callback_data='add_flat_metro')
    description_btn = InlineKeyboardButton('Описание', callback_data='add_flat_description')
    photo_btn = InlineKeyboardButton('Добавить фото', callback_data='add_flat_photo')
    finish_btn = InlineKeyboardButton('Добавить квартиру', callback_data='add_flat_finish')
    exit_btn = InlineKeyboardButton('Прервать добавление', callback_data='add_flat_exit')

    add_flat_keyboard.row(price_btn, rooms_btn, square_btn)
    add_flat_keyboard.row(address_btn, floor_btn)
    add_flat_keyboard.row(metro_btn, description_btn)
    add_flat_keyboard.add(photo_btn)
    add_flat_keyboard.add(finish_btn)
    add_flat_keyboard.add(exit_btn)

    return add_flat_keyboard


def get_pagination_keyboard():
    pagination_keyboard = InlineKeyboardMarkup()
    left_btn = InlineKeyboardButton('<<', callback_data='pagination_left')
    right_btn = InlineKeyboardButton('>>', callback_data='pagination_right')
    cancel_btn = InlineKeyboardButton('Отменить', callback_data='pagination_cancel')

    pagination_keyboard.row(left_btn, right_btn)
    pagination_keyboard.add(cancel_btn)

    return pagination_keyboard


def get_flats_filter_keyboard():
    show_flat_keyboard = InlineKeyboardMarkup()
    price_btn = InlineKeyboardButton('Цена', callback_data='show_flats_price')
    rooms_btn = InlineKeyboardButton('Комнаты', callback_data='show_flats_rooms')
    square_btn = InlineKeyboardButton('Площадь', callback_data='show_flats_square')
    metro_btn = InlineKeyboardButton('Ближайшее метро', callback_data='show_flats_metro')
    finish_btn = InlineKeyboardButton('Найти квартиры', callback_data='show_flats_finish')
    exit_btn = InlineKeyboardButton('Прервать поиск', callback_data='show_flats_exit')

    show_flat_keyboard.row(price_btn, rooms_btn)
    show_flat_keyboard.add(square_btn)
    show_flat_keyboard.add(metro_btn)
    show_flat_keyboard.add(finish_btn)
    show_flat_keyboard.add(exit_btn)

    return show_flat_keyboard


def get_landlord_info_keyboard():
    get_landlord_keyboard = InlineKeyboardMarkup()
    rating_btn = InlineKeyboardButton('Поставить оценку', callback_data='get_landlord_rating')
    exit_btn = InlineKeyboardButton('Отмена', callback_data='get_landlord_cancel')

    get_landlord_keyboard.add(rating_btn)
    get_landlord_keyboard.add(exit_btn)

    return get_landlord_keyboard

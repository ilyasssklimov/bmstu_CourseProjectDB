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


def get_pagination_keyboard(collapse: bool = False):
    pagination_keyboard = InlineKeyboardMarkup()
    left_btn = InlineKeyboardButton('<<', callback_data='pagination_left')
    right_btn = InlineKeyboardButton('>>', callback_data='pagination_right')
    pagination_keyboard.row(left_btn, right_btn)

    if not collapse:
        like_flat = InlineKeyboardButton('Нравится', callback_data='pagination_like')
        pagination_keyboard.add(like_flat)

    cancel_btn = InlineKeyboardButton('Отменить', callback_data='pagination_cancel')
    pagination_keyboard.add(cancel_btn)

    return pagination_keyboard


def get_flats_filter_keyboard():
    show_flat_keyboard = InlineKeyboardMarkup()
    price_btn = InlineKeyboardButton('Цена', callback_data='show_flats_price')
    rooms_btn = InlineKeyboardButton('Комнаты', callback_data='show_flats_rooms')
    square_btn = InlineKeyboardButton('Площадь', callback_data='show_flats_square')
    metro_btn = InlineKeyboardButton('Ближайшее метро', callback_data='show_flats_metro')
    finish_btn = InlineKeyboardButton('Найти квартиры', callback_data='show_flats_finish')
    subscribe_btn = InlineKeyboardButton('Подписаться', callback_data='show_flats_subscribe')
    exit_btn = InlineKeyboardButton('Прервать поиск', callback_data='show_flats_exit')

    show_flat_keyboard.row(price_btn, rooms_btn)
    show_flat_keyboard.add(square_btn)
    show_flat_keyboard.add(metro_btn)
    show_flat_keyboard.add(finish_btn)
    show_flat_keyboard.add(subscribe_btn)
    show_flat_keyboard.add(exit_btn)

    return show_flat_keyboard


def get_landlord_info_keyboard():
    get_landlord_keyboard = InlineKeyboardMarkup()
    rating_btn = InlineKeyboardButton('Поставить оценку', callback_data='get_landlord_rating')
    subscribe_btn = InlineKeyboardButton('Подписаться / Отписаться', callback_data='get_landlord_subscribe')
    exit_btn = InlineKeyboardButton('Отмена', callback_data='get_landlord_cancel')

    get_landlord_keyboard.add(rating_btn)
    get_landlord_keyboard.add(subscribe_btn)
    get_landlord_keyboard.add(exit_btn)

    return get_landlord_keyboard


def get_add_neighborhood_keyboard():
    add_neighborhood_keyboard = InlineKeyboardMarkup()
    neighbors_btn = InlineKeyboardButton('Соседи', callback_data='add_neighborhood_neighbors')
    price_btn = InlineKeyboardButton('Цена', callback_data='add_neighborhood_price')
    place_btn = InlineKeyboardButton('Местоположение', callback_data='add_neighborhood_place')
    sex_btn = InlineKeyboardButton('Пол', callback_data='add_neighborhood_sex')
    preferences_btn = InlineKeyboardButton('Личные предпочтения', callback_data='add_neighborhood_preferences')
    finish_btn = InlineKeyboardButton('Добавить объявление', callback_data='add_neighborhood_finish')
    exit_btn = InlineKeyboardButton('Прервать добавление', callback_data='add_neighborhood_exit')

    add_neighborhood_keyboard.row(neighbors_btn, price_btn)
    add_neighborhood_keyboard.row(place_btn, sex_btn)
    add_neighborhood_keyboard.row(preferences_btn)
    add_neighborhood_keyboard.add(finish_btn)
    add_neighborhood_keyboard.add(exit_btn)

    return add_neighborhood_keyboard


def get_expanded_sex_keyboard():
    sex_keyboard = InlineKeyboardMarkup()
    male = InlineKeyboardButton('Мужской', callback_data='expanded_sex_male')
    female = InlineKeyboardButton('Женский', callback_data='expanded_sex_female')
    no_male = InlineKeyboardButton('Не имеет значения', callback_data='expanded_sex_no_male')
    sex_keyboard.row(male, female)
    sex_keyboard.add(no_male)

    return sex_keyboard


def get_neighborhoods_filter_keyboard():
    show_neighborhood_keyboard = InlineKeyboardMarkup()
    neighbors_btn = InlineKeyboardButton('Соседи', callback_data='show_neighborhoods_neighbors')
    price_btn = InlineKeyboardButton('Цена', callback_data='show_neighborhoods_price')
    sex_btn = InlineKeyboardButton('Пол', callback_data='show_neighborhoods_sex')
    finish_btn = InlineKeyboardButton('Найти объявления', callback_data='show_neighborhoods_finish')
    exit_btn = InlineKeyboardButton('Прервать поиск', callback_data='show_neighborhoods_exit')

    show_neighborhood_keyboard.row(neighbors_btn, price_btn, sex_btn)
    show_neighborhood_keyboard.add(finish_btn)
    show_neighborhood_keyboard.add(exit_btn)

    return show_neighborhood_keyboard


def get_add_goods_keyboard():
    add_goods_keyboard = InlineKeyboardMarkup()
    name_btn = InlineKeyboardButton('Название', callback_data='add_goods_name')
    price_btn = InlineKeyboardButton('Цена', callback_data='add_goods_price')
    condition_btn = InlineKeyboardButton('Состояние', callback_data='add_goods_condition')
    bargain_btn = InlineKeyboardButton('Торг', callback_data='add_goods_bargain')
    finish_btn = InlineKeyboardButton('Добавить объявление', callback_data='add_goods_finish')
    exit_btn = InlineKeyboardButton('Прервать добавление', callback_data='add_goods_exit')

    add_goods_keyboard.row(name_btn, price_btn)
    add_goods_keyboard.row(condition_btn, bargain_btn)
    add_goods_keyboard.add(finish_btn)
    add_goods_keyboard.add(exit_btn)

    return add_goods_keyboard


def get_condition_keyboard():
    condition_keyboard = InlineKeyboardMarkup()
    excellent = InlineKeyboardButton('Отличное', callback_data='condition_excellent')
    good = InlineKeyboardButton('Хорошее', callback_data='condition_good')
    satisfactory = InlineKeyboardButton('Удовлетворительное', callback_data='condition_satisfactory')
    unsatisfactory = InlineKeyboardButton('Неудовлетворительное', callback_data='condition_unsatisfactory')
    terrible = InlineKeyboardButton('Ужасное', callback_data='condition_terrible')
    condition_keyboard.add(excellent)
    condition_keyboard.add(good)
    condition_keyboard.add(satisfactory)
    condition_keyboard.add(unsatisfactory)
    condition_keyboard.add(terrible)

    return condition_keyboard


def get_bargain_keyboard():
    bargain_keyboard = InlineKeyboardMarkup()
    yes = InlineKeyboardButton('Да', callback_data='bargain_yes')
    no = InlineKeyboardButton('Нет', callback_data='bargain_no')
    bargain_keyboard.row(yes, no)

    return bargain_keyboard

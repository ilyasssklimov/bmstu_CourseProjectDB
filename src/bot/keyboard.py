from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


register_tenant_keyboard = InlineKeyboardMarkup()
name_btn = InlineKeyboardButton('Полное имя', callback_data='register_tenant_name')
sex_btn = InlineKeyboardButton('Пол', callback_data='register_tenant_sex')
city_btn = InlineKeyboardButton('Город', callback_data='register_tenant_city')
qualities_btn = InlineKeyboardButton('Персональные качества', callback_data='register_tenant_qualities')
age_btn = InlineKeyboardButton('Возраст', callback_data='register_tenant_age')
solvency_btn = InlineKeyboardButton('Платежеспособность', callback_data='register_tenant_solvency')
finish_btn = InlineKeyboardButton('Завершить регистрацию', callback_data='register_tenant_finish')
register_tenant_keyboard.row(name_btn, age_btn)
register_tenant_keyboard.row(sex_btn, city_btn)
register_tenant_keyboard.add(qualities_btn)
register_tenant_keyboard.add(solvency_btn)
register_tenant_keyboard.add(finish_btn)


sex_keyboard = InlineKeyboardMarkup()
male = InlineKeyboardButton('Мужской', callback_data='sex_male')
female = InlineKeyboardButton('Женский', callback_data='sex_female')
sex_keyboard.row(male, female)


solvency_keyboard = InlineKeyboardMarkup()
yes = InlineKeyboardButton('Да', callback_data='solvency_yes')
no = InlineKeyboardButton('Нет', callback_data='solvency_no')
solvency_keyboard.row(yes, no)

from enum import Enum
import os


class EntityType(Enum):
    NO_TYPE = 0
    TENANT = 1
    LANDLORD = 2
    FLAT = 3
    NEIGHBORHOOD = 4
    GOODS = 5

    def __eq__(self, other):
        if self.__class__ is other.__class__ and self.value == other.value:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)


API_TOKEN = os.getenv('HOSTEL_TOKEN_API')
IMG_PATH = './img'


TENANT_FIELDS = {
    'name': 'Имя',
    'sex': 'Пол',
    'city': 'Город',
    'age': 'Возраст'
}

ALL_TENANT_FIELDS = {
    'name': 'Имя',
    'sex': 'Пол',
    'city': 'Город',
    'qualities': 'Персональные качества',
    'age': 'Возраст',
    'solvency': 'Платежеспособность'
}


LANDLORD_FIELDS = {
    'name': 'Имя',
    'city': 'Город',
    'rating': 'Рейтинг',
    'age': 'Возраст',
    'phone': 'Телефон'
}

ALL_LANDLORD_FIELDS = {
    'name': 'Имя',
    'city': 'Город',
    'age': 'Возраст',
    'phone': 'Телефон'
}


FLAT_FIELDS = {
    'price': 'Цена',
    'rooms': 'Комнаты',
    'square': 'Площадь',
    'address': 'Адрес'
}

ALL_FLAT_FIELDS = {
    'price': 'Цена',
    'rooms': 'Комнаты',
    'square': 'Площадь',
    'address': 'Адрес',
    'metro': 'Ближайшее метро',
    'floor': 'Этаж',
    'max_floor': 'Максимальный этаж',
    'description': 'Описание'
}

FILTER_FLAT_FIELDS = {
    'price': 'Цена',
    'rooms': 'Комнаты',
    'square': 'Площадь',
    'metro': 'Метро'
}


NEIGHBORHOOD_FIELDS = {
    'neighbors': 'Соседи',
    'price': 'Цена',
    'sex': 'Пол'
}

ALL_NEIGHBORHOOD_FIELDS = {
    'neighbors': 'Соседи',
    'price': 'Цена',
    'place': 'Местоположение',
    'sex': 'Пол',
    'preferences': 'Личные предпочтения'
}

FILTER_NEIGHBORHOOD_FIELDS = {
    'neighbors': 'Соседи',
    'price': 'Цена',
    'sex': 'Пол'
}


GOODS_FIELDS = {
    'name': 'Название',
    'price': 'Цена',
    'condition': 'Состояние'
}

ALL_GOODS_FIELDS = {
    'name': 'Название',
    'price': 'Цена',
    'condition': 'Состояние',
    'bargain': 'Торг'
}

FILTER_GOODS_FIELDS = {
    'price': 'Цена',
    'condition': 'Состояние'
}

GOODS_CONDITIONS = {
    'E': 'Отличное',
    'G': 'Хорошее',
    'S': 'Удовлетворительное',
    'U': 'Неудовлетворительное',
    'T': 'Ужасное'
}

GOODS_BARGAIN = {
    True: 'Да',
    False: 'Нет'
}

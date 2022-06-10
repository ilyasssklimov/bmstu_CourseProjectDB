from enum import Enum
from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterTenantStates(StatesGroup):
    START_STATE = State()
    NAME_STATE = State()
    SEX_STATE = State()
    CITY_STATE = State()
    QUALITIES_STATE = State()
    AGE_STATE = State()
    SOLVENCY_STATE = State()

    @classmethod
    def get_states(cls):
        return map(lambda x: x.state, cls.all_states)


class RegisterLandlordStates(StatesGroup):
    START_STATE = State()
    NAME_STATE = State()
    CITY_STATE = State()
    AGE_STATE = State()

    @classmethod
    def get_states(cls):
        return map(lambda x: x.state, cls.all_states)


class EntityTypes(Enum):
    TENANT = 1
    LANDLORD = 2


class RolesDB(Enum):
    GUEST = 1
    TENANT = 2
    LANDLORD = 3
    ADMIN = 4

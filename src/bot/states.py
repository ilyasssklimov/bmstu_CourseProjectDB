from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterTenantStates(StatesGroup):
    START_STATE = State()
    NAME_STATE = State()
    SEX_STATE = State()
    CITY_STATE = State()
    QUALITIES_STATE = State()
    AGE_STATE = State()
    SOLVENCY_STATE = State()

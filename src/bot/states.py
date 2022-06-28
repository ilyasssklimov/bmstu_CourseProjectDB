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
    PHONE_STATE = State()

    @classmethod
    def get_states(cls):
        return map(lambda x: x.state, cls.all_states)


class AddFlatStates(StatesGroup):
    START_STATE = State()
    PRICE_STATE = State()
    SQUARE_STATE = State()
    ADDRESS_STATE = State()
    METRO_STATE = State()
    FLOOR_STATE = State()
    DESCRIPTION_STATE = State()
    PHOTO_STATE = State()

    @classmethod
    def get_states(cls):
        return map(lambda x: x.state, cls.all_states)

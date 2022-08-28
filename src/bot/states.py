from aiogram.dispatcher.filters.state import State, StatesGroup


class SayNoToHostelStates(StatesGroup):
    @classmethod
    def get_states(cls):
        return map(lambda x: x.state, cls.all_states)


class RegisterTenantStates(SayNoToHostelStates):
    START_STATE = State()
    NAME_STATE = State()
    SEX_STATE = State()
    CITY_STATE = State()
    QUALITIES_STATE = State()
    AGE_STATE = State()
    SOLVENCY_STATE = State()


class RegisterLandlordStates(SayNoToHostelStates):
    START_STATE = State()
    NAME_STATE = State()
    CITY_STATE = State()
    AGE_STATE = State()
    PHONE_STATE = State()


class AddFlatStates(SayNoToHostelStates):
    START_STATE = State()
    PRICE_STATE = State()
    ROOMS_STATE = State()
    SQUARE_STATE = State()
    ADDRESS_STATE = State()
    METRO_STATE = State()
    FLOOR_STATE = State()
    DESCRIPTION_STATE = State()
    PHOTO_STATE = State()


class ShowFlatsStates(SayNoToHostelStates):
    PAGINATION_STATE = State()
    START_STATE = State()
    PRICE_STATE = State()
    ROOMS_STATE = State()
    SQUARE_STATE = State()
    METRO_STATE = State()


class GetLandlordInfoStates(SayNoToHostelStates):
    NAME_STATE = State()
    START_STATE = State()
    RATING_STATE = State()


class AddNeighborhoodStates(SayNoToHostelStates):
    START_STATE = State()
    NEIGHBORS_STATE = State()
    PRICE_STATE = State()
    PLACE_STATE = State()
    SEX_STATE = State()
    PREFERENCES_STATE = State()


class ShowNeighborhoodsStates(SayNoToHostelStates):
    PAGINATION_STATE = State()
    START_STATE = State()
    NEIGHBORS_STATE = State()
    PRICE_STATE = State()
    SEX_STATE = State()

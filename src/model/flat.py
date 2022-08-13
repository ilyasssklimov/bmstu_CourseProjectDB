from src.model.model import BaseModel


class Flat(BaseModel):
    def __init__(self, flat_id=-1, owner_id=-1, price=-1, rooms=-1, square=-1, address='', metro='',
                 floor=-1, max_floor=-1, description=''):
        super().__init__(
            id=flat_id,
            owner_id=owner_id,
            price=price,
            rooms=rooms,
            square=square,
            address=address,
            metro=metro,
            floor=floor,
            max_floor=max_floor,
            description=description
        )

    @property
    def id(self):
        return self._args['id']

    @property
    def owner_id(self):
        return self._args['owner_id']

    @property
    def price(self):
        return self._args['price']

    @property
    def rooms(self):
        return self._args['rooms']

    @property
    def square(self):
        return self._args['square']

    @property
    def address(self):
        return self._args['address']

    @property
    def metro(self):
        return self._args['metro']

    @property
    def floor(self):
        return self._args['floor']

    @property
    def max_floor(self):
        return self._args['max_floor']

    @property
    def description(self):
        return self._args['description']

    def set_id(self, value):
        self._args['id'] = value

    def set_owner_id(self, value):
        self._args['owner_id'] = value

    def set_price(self, value):
        self._args['price'] = value

    def set_rooms(self, value):
        self._args['rooms'] = value

    def set_square(self, value):
        self._args['square'] = value

    def set_address(self, value):
        self._args['address'] = value

    def set_metro(self, value):
        self._args['metro'] = value

    def set_floor(self, value):
        self._args['floor'] = value

    def set_max_floor(self, value):
        self._args['max_floor'] = value

    def set_description(self, value):
        self._args['description'] = value

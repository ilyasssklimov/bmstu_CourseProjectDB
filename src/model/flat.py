class Flat:
    def __init__(self, flat_id=-1, owner_id=-1, price=-1, rooms=-1, square=-1, address='', metro='',
                 floor=-1, max_floor=-1, description=''):
        self.__args = {
            'id': flat_id,
            'owner_id': owner_id,
            'price': price,
            'rooms': rooms,
            'square': square,
            'address': address,
            'metro': metro,
            'floor': floor,
            'max_floor': max_floor,
            'description': description
        }

    @property
    def id(self):
        return self.__args['id']

    @property
    def owner_id(self):
        return self.__args['owner_id']

    @property
    def price(self):
        return self.__args['price']

    @property
    def rooms(self):
        return self.__args['rooms']

    @property
    def square(self):
        return self.__args['square']

    @property
    def address(self):
        return self.__args['address']

    @property
    def metro(self):
        return self.__args['metro']

    @property
    def floor(self):
        return self.__args['floor']

    @property
    def max_floor(self):
        return self.__args['max_floor']

    @property
    def description(self):
        return self.__args['description']

    def get_params(self):
        return list(self.__args.values())

    def set_id(self, value):
        self.__args['id'] = value

    def set_owner_id(self, value):
        self.__args['owner_id'] = value

    def set_price(self, value):
        self.__args['price'] = value

    def set_rooms(self, value):
        self.__args['rooms'] = value

    def set_square(self, value):
        self.__args['square'] = value

    def set_address(self, value):
        self.__args['address'] = value

    def set_metro(self, value):
        self.__args['metro'] = value

    def set_floor(self, value):
        self.__args['floor'] = value

    def set_max_floor(self, value):
        self.__args['max_floor'] = value

    def set_description(self, value):
        self.__args['description'] = value

    def __getitem__(self, item):
        return self.get_params()[item]

    def __setitem__(self, key, value):
        self.__args[key] = value

    def __len__(self):
        return len(self.__args)

    def __bool__(self):
        return self.id != -1

    def __eq__(self, other):
        return (
            self.owner_id == other.owner_id and
            self.price == other.price and
            self.rooms == other.rooms and
            self.square == other.square and
            self.address == other.address and
            self.metro == other.metro and
            self.floor == other.floor and
            self.max_floor == other.max_floor and
            self.description == other.description
        )

    def __str__(self):
        return f'Flat (id = {self.id}, owner_id = {self.owner_id}, price = {self.price}, ' \
               f'rooms = {self.rooms}, square = {self.square}, address = {self.address},' \
               f' metro = {self.metro}, floor = {self.floor} / {self.max_floor}, ' \
               f'description = {self.description})'

    def __repr__(self):
        return str(self)

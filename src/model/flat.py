class Flat:
    def __init__(self, flat_id=-1, owner_id=-1, price=-1, rooms=-1, square=-1, address='', metro='',
                 floor=-1, max_floor=-1, description=''):
        self.__args = {
            0: flat_id,
            1: owner_id,
            2: price,
            3: rooms,
            4: square,
            5: address,
            6: metro,
            7: floor,
            8: max_floor,
            9: description
        }

    @property
    def flat_id(self):
        return self.__args[0]

    @property
    def owner_id(self):
        return self.__args[1]

    @property
    def price(self):
        return self.__args[2]

    @property
    def rooms(self):
        return self.__args[3]

    @property
    def square(self):
        return self.__args[4]

    @property
    def address(self):
        return self.__args[5]

    @property
    def metro(self):
        return self.__args[6]

    @property
    def floor(self):
        return self.__args[7]

    @property
    def max_floor(self):
        return self.__args[8]

    @property
    def description(self):
        return self.__args[9]

    def get_params(self):
        return list(self.__args.values())

    def set_owner_id(self, value):
        self.__args[1] = value

    def set_price(self, value):
        self.__args[2] = value

    def set_rooms(self, value):
        self.__args[3] = value

    def set_square(self, value):
        self.__args[4] = value

    def set_address(self, value):
        self.__args[5] = value

    def set_metro(self, value):
        self.__args[6] = value

    def set_floor(self, value):
        self.__args[7] = value

    def set_max_floor(self, value):
        self.__args[8] = value

    def set_description(self, value):
        self.__args[9] = value

    def __getitem__(self, item):
        if item in self.__args:
            return self.__args[item]
        else:
            return None

    def __setitem__(self, key, value):
        self.__args[key] = value

    def __len__(self):
        return len(self.__args)

    def __bool__(self):
        return self.__args[0] != -1

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
        return f'Flat (id = {self.__args[0]}, owner_id = {self.__args[1]}, price = {self.__args[2]}, ' \
               f'rooms = {self.__args[3]}, square = {self.__args[4]}, address = {self.__args[5]},' \
               f' metro = {self.__args[6]}, floor = {self.__args[7]} / {self.__args[8]}, ' \
               f'description = {self.__args[9]})'

    def __repr__(self):
        return str(self)

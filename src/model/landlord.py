class Landlord:
    def __init__(self, landlord_id=-1, full_name='', city='', rating=0.0, age=-1, phone=''):
        self.__args = {
            0: landlord_id,
            1: full_name,
            2: city,
            3: rating,
            4: age,
            5: phone
        }

    @property
    def id(self):
        return self.__args[0]

    @property
    def full_name(self):
        return self.__args[1]

    @property
    def city(self):
        return self.__args[2]

    @property
    def rating(self):
        return self.__args[3]

    @property
    def age(self):
        return self.__args[4]

    @property
    def phone(self):
        return self.__args[5]

    def get_params(self):
        return list(self.__args.values())

    def set_id(self, value):
        self.__args[0] = value

    def set_full_name(self, value):
        self.__args[1] = value

    def set_city(self, value):
        self.__args[2] = value

    def set_rating(self, value):
        self.__args[3] = value

    def set_age(self, value):
        self.__args[4] = value

    def set_phone(self, value):
        self.__args[5] = value

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
            self.id == other.id and
            self.full_name == other.full_name and
            self.city == other.city and
            self.rating == other.rating and
            self.age == other.age and
            self.phone == other.phone
        )

    def __str__(self):
        return f'Landlord (id = {self.__args[0]}, full_name = {self.__args[1]}, city = {self.__args[2]}, ' \
               f'rating = {self.__args[3]}, age = {self.__args[4]}, number = {self.__args[5]})'

    def __repr__(self):
        return str(self)

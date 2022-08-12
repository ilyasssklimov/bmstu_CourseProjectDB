class Landlord:
    def __init__(self, landlord_id=-1, full_name='', city='', rating=0.0, age=-1, phone='', username=''):
        self.__args = {
            'id': landlord_id,
            'full_name': full_name,
            'city': city,
            'rating': rating,
            'age': age,
            'phone': phone,
            'username': username
        }

    @property
    def id(self):
        return self.__args['id']

    @property
    def full_name(self):
        return self.__args['full_name']

    @property
    def city(self):
        return self.__args['city']

    @property
    def rating(self):
        return self.__args['rating']

    @property
    def age(self):
        return self.__args['age']

    @property
    def phone(self):
        return self.__args['phone']

    @property
    def username(self):
        return self.__args['username']

    def get_params(self):
        return list(self.__args.values())

    def set_id(self, value):
        self.__args['id'] = value

    def set_full_name(self, value):
        self.__args['full_name'] = value

    def set_city(self, value):
        self.__args['city'] = value

    def set_rating(self, value):
        self.__args['rating'] = value

    def set_age(self, value):
        self.__args['age'] = value

    def set_phone(self, value):
        self.__args['phone'] = value

    def set_username(self, value):
        self.__args['username'] = value

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
        return self.id != -1

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
        return f'Landlord (id = {self.id}, full_name = {self.full_name}, city = {self.city}, ' \
               f'rating = {self.rating}, age = {self.age}, phone = {self.phone}, username = {self.username})'

    def __repr__(self):
        return str(self)

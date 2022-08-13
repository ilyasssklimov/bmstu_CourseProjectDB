class Tenant:
    def __init__(self, tenant_id=-1, full_name='', sex='', city='', qualities='', age=-1, solvency='None'):
        self.__args = {
            'id': tenant_id,
            'full_name': full_name,
            'sex': sex,
            'city': city,
            'qualities': qualities,
            'age': age,
            'solvency': solvency
        }

    @property
    def id(self):
        return self.__args['id']

    @property
    def full_name(self):
        return self.__args['full_name']

    @property
    def sex(self):
        return self.__args['sex']

    @property
    def city(self):
        return self.__args['city']

    @property
    def qualities(self):
        return self.__args['qualities']

    @property
    def age(self):
        return self.__args['age']

    @property
    def solvency(self):
        return self.__args['solvency']

    def get_params(self):
        return list(self.__args.values())

    def get_names(self):
        return list(self.__args.keys())

    def set_id(self, value):
        self.__args['id'] = value

    def set_full_name(self, value):
        self.__args['full_name'] = value

    def set_sex(self, value):
        self.__args['sex'] = value

    def set_city(self, value):
        self.__args['city'] = value

    def set_qualities(self, value):
        self.__args['qualities'] = value

    def set_age(self, value):
        self.__args['value'] = value

    def set_solvency(self, value):
        self.__args['solvency'] = value

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
            self.sex == other.sex and
            self.city == other.city and
            self.qualities == other.qualities and
            self.age == other.age and
            ((not self.solvency and other.solvency == 'null') or
             str(self.solvency).lower() == str(other.solvency).lower())
        )

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f'Tenant (id = {self.id}, full_name = {self.full_name}, sex = {self.sex}, city = ' \
               f'{self.city}, qualities = {self.qualities}, age = {self.age}, solvency = {self.solvency})'

    def __repr__(self):
        return str(self)

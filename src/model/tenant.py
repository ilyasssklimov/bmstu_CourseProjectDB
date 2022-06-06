class Tenant:
    def __init__(self, tenant_id=-1, full_name='', sex='', city='', qualities='', age=-1, solvency='None'):
        self.__args = {
            0: tenant_id,
            1: full_name,
            2: sex,
            3: city,
            4: qualities,
            5: age,
            6: solvency
        }

    @property
    def id(self):
        return self.__args[0]

    @property
    def full_name(self):
        return self.__args[1]

    @property
    def sex(self):
        return self.__args[2]

    @property
    def city(self):
        return self.__args[3]

    @property
    def qualities(self):
        return self.__args[4]

    @property
    def age(self):
        return self.__args[5]

    @property
    def solvency(self):
        return self.__args[6]

    def set_id(self, value):
        self.__args[0] = value

    def set_full_name(self, value):
        self.__args[1] = value

    def set_sex(self, value):
        self.__args[2] = value

    def set_city(self, value):
        self.__args[3] = value

    def set_qualities(self, value):
        self.__args[4] = value

    def set_age(self, value):
        self.__args[5] = value

    def set_solvency(self, value):
        self.__args[6] = value

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
            self.sex == other.sex and
            self.city == other.city and
            self.qualities == other.qualities and
            self.age == other.age and
            ((not self.solvency and other.solvency == 'null') or str(self.solvency).lower() == other.solvency.lower())
        )

    def __str__(self):
        return f'Tenant (id = {self.__args[0]}, full_name = {self.__args[1]}, sex = {self.__args[2]}, city = ' \
               f'{self.__args[3]}, qualities = {self.__args[4]}, age = {self.__args[5]}, solvency = {self.__args[6]})'

    def __repr__(self):
        return str(self)

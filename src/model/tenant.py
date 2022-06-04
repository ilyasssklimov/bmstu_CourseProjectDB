class Tenant:
    def __init__(self, full_name: str, sex: str, city: str, qualities: str, age: int, solvency: bool):
        self.__full_name = full_name
        self.__sex = sex
        self.__city = city
        self.__qualities = qualities
        self.__age = age
        self.__solvency = solvency

    @property
    def full_name(self):
        return self.__full_name

    @property
    def sex(self):
        return self.__sex

    @property
    def city(self):
        return self.__city

    @property
    def qualities(self):
        return self.__qualities

    @property
    def age(self):
        return self.__age

    @property
    def solvency(self):
        return self.__solvency

    def set_full_name(self, value):
        self.__full_name = value

    def set_sex(self, value):
        self.__sex = value

    def set_city(self, value):
        self.__city = value

    def set_qualities(self, value):
        self.__qualities = value

    def set_age(self, value):
        self.__age = value

    def set_solvency(self, value):
        self.__solvency = value

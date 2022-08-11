from faker import Faker
from random import randint, choice, uniform
from src.bot.config import EntityType as EType
from src.database.database import BaseDatabase
from src.generate_data.config import PHONE_CODE, USER_ID_RANGE, USER_AGE_RANGE, LANDLORD_RATING_RANGE


class GenerateData:
    def __init__(self, db: BaseDatabase):
        self.__db = db
        self.faker = Faker('ru_RU')

    def generate_users(self, user_type: EType, n: int = 100):
        for i in range(n):
            user_id = randint(*USER_ID_RANGE)
            full_name = self.faker.name()
            city = self.faker.city()
            age = randint(*USER_AGE_RANGE)

            if user_type == EType.TENANT:
                sex = choice(['M', 'F'])
                qualities = self.faker.text(50)
                solvency = choice([True, False])
                self.__db.add_tenant(user_id, full_name, sex, city, qualities, age, solvency)
            elif user_type == EType.LANDLORD:
                en_faker = Faker()
                rating = round(uniform(*LANDLORD_RATING_RANGE), 1)
                phone = PHONE_CODE + ''.join([str(randint(0, 9)) for _ in range(10)])
                username = en_faker.user_name()
                self.__db.add_landlord(user_id, full_name, city, rating, age, phone, username)
            else:
                raise ValueError('User type can be TENANT or LANDLORD')

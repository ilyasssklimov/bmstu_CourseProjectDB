import random
import src.generate_data.config as cfg
from faker import Faker
from random import randint, choice, uniform
from src.bot.config import EntityType as EType
from src.database.database import BaseDatabase
from src.generate_data.flat import ParserFlats
from src.model.landlord import Landlord
from src.model.neighborhood import Neighborhood
from src.model.tenant import Tenant
from src.repository.landlord import LandlordRepository
from src.repository.neighborhood import NeighborhoodRepository
from src.repository.tenant import TenantRepository


class DataGenerator:
    def __init__(self, db: BaseDatabase):
        self.__db = db
        self.__landlord_repo = LandlordRepository(db)
        self.__tenant_repo = TenantRepository(db)
        self.__neighborhood_repo = NeighborhoodRepository(db)

        self.faker = Faker('ru_RU')
        self.__tenant_ids = [tenant.id for tenant in self.__tenant_repo.get_tenants()]

    def generate_users(self, user_type: EType, n: int = 100):
        for i in range(n):
            user_id = randint(*cfg.USER_ID_RANGE)
            full_name = self.faker.name()
            city = self.faker.city()
            age = randint(*cfg.USER_AGE_RANGE)

            if user_type == EType.TENANT:
                sex = choice(['M', 'F'])
                qualities = self.faker.text(50)
                solvency = choice([True, False])
                tenant = Tenant(user_id, full_name, sex, city, qualities, age, solvency)
                self.__tenant_repo.add_tenant(tenant)
            elif user_type == EType.LANDLORD:
                en_faker = Faker()
                rating = round(uniform(*cfg.LANDLORD_RATING_RANGE), 1)
                phone = cfg.PHONE_CODE + ''.join([str(randint(0, 9)) for _ in range(10)])
                username = en_faker.user_name()
                landlord = Landlord(user_id, full_name, city, rating, age, phone, username)
                self.__landlord_repo.add_landlord(landlord)
            else:
                raise ValueError('User type can be TENANT or LANDLORD')

    def parse_flats(self, url: str, n: int = 100):
        parser_flats = ParserFlats(self.__db)
        parser_flats.add_flats(url, n)
        del parser_flats

    def generate_neighborhoods(self, n: int = 100):
        for i in range(n):
            tenant_id = random.choice(self.__tenant_ids)
            neighbors = randint(*cfg.NEIGHBOR_RANGE)
            price = randint(*cfg.NEIGHBORHOOD_PRICE_RANGE)
            place = self.faker.text(25)
            sex = choice(['M', 'F', 'N'])
            preferences = self.faker.text(50)
            neighborhood = Neighborhood(-1, tenant_id, neighbors, price, place, sex, preferences)
            self.__neighborhood_repo.add_neighborhood(neighborhood)

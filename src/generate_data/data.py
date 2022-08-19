import random
import src.generate_data.config as cfg
from faker import Faker
from random import randint, choice, uniform
from src.bot.config import EntityType as EType
from src.database.database import BaseDatabase
from src.generate_data.flat import ParserFlats
from src.model.goods import Goods
from src.model.landlord import Landlord
from src.model.neighborhood import Neighborhood
from src.model.tenant import Tenant
from src.repository.goods import GoodsRepository
from src.repository.landlord import LandlordRepository
from src.repository.neighborhood import NeighborhoodRepository
from src.repository.tenant import TenantRepository


class DataGenerator:
    def __init__(self, db: BaseDatabase):
        self.__db = db
        self.__landlord_repo = LandlordRepository(db)
        self.__tenant_repo = TenantRepository(db)
        self.__neighborhood_repo = NeighborhoodRepository(db)
        self.__goods_repo = GoodsRepository(db)

        self.faker = Faker('ru_RU')

    def generate_users(self, user_type: EType, n: int = 100) -> int:
        en_faker = Faker()
        count = 0
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
                if self.__tenant_repo.add_tenant(tenant):
                    count += 1
            elif user_type == EType.LANDLORD:
                rating = round(uniform(*cfg.LANDLORD_RATING_RANGE), 1)
                phone = cfg.PHONE_CODE + ''.join([str(randint(0, 9)) for _ in range(10)])
                username = en_faker.user_name()
                landlord = Landlord(user_id, full_name, city, rating, age, phone, username)
                if self.__landlord_repo.add_landlord(landlord):
                    count += 1
            else:
                raise ValueError('User type can be TENANT or LANDLORD')

        return count

    def parse_flats(self, url: str, n: int = 100):
        parser_flats = ParserFlats(self.__db)
        return parser_flats.add_flats(url, n)

    def generate_neighborhoods(self, n: int = 100) -> int:
        tenant_ids = [tenant.id for tenant in self.__tenant_repo.get_tenants()]
        if not tenant_ids:
            return 0

        count = 0
        for i in range(n):
            tenant_id = random.choice(tenant_ids)
            neighbors = randint(*cfg.NEIGHBOR_RANGE)
            price = randint(*cfg.NEIGHBORHOOD_PRICE_RANGE)
            place = self.faker.address()
            sex = choice(['M', 'F', 'N'])
            preferences = self.faker.text(50)
            neighborhood = Neighborhood(-1, tenant_id, neighbors, price, place, sex, preferences)
            if self.__neighborhood_repo.add_neighborhood(neighborhood):
                count += 1

        return count

    def generate_goods(self, n: int = 100) -> int:
        tenant_ids = [tenant.id for tenant in self.__tenant_repo.get_tenants()]
        if not tenant_ids:
            return 0

        count = 0
        for i in range(n):
            owner_id = random.choice(tenant_ids)
            name = self.faker.text(25)
            price = randint(*cfg.GOODS_PRICE_RANGE)
            condition = choice(['E', 'G', 'S', 'U', 'T'])
            bargain = choice([True, False])
            goods = Goods(-1, owner_id, name, price, condition, bargain)
            if self.__goods_repo.add_goods(goods):
                count += 1

        return count

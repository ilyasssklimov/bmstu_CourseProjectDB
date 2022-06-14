from faker import Faker
from random import randint, choice
from src.database.database import PostgresDB


def generate_tenants(db: PostgresDB, n=100):
    faker = Faker('ru_RU')
    for i in range(n):
        tenant_id = randint(1000000, 10000000)
        full_name = faker.name()
        sex = choice(['M', 'F'])
        city = faker.city()
        qualities = faker.text(50)
        age = randint(14, 100)
        solvency = choice([True, False])
        db.add_tenant(tenant_id, full_name, sex, city, qualities, age, solvency)


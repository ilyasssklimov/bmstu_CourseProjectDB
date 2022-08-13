from src.model.model import BaseModel


class Landlord(BaseModel):
    def __init__(self, landlord_id=-1, full_name='', city='', rating=0.0, age=-1, phone='', username=''):
        super().__init__(
            id=landlord_id,
            full_name=full_name,
            city=city,
            rating=rating,
            age=age,
            phone=phone,
            username=username
        )

    @property
    def id(self):
        return self._args['id']

    @property
    def full_name(self):
        return self._args['full_name']

    @property
    def city(self):
        return self._args['city']

    @property
    def rating(self):
        return self._args['rating']

    @property
    def age(self):
        return self._args['age']

    @property
    def phone(self):
        return self._args['phone']

    @property
    def username(self):
        return self._args['username']

    def set_id(self, value):
        self._args['id'] = value

    def set_full_name(self, value):
        self._args['full_name'] = value

    def set_city(self, value):
        self._args['city'] = value

    def set_rating(self, value):
        self._args['rating'] = value

    def set_age(self, value):
        self._args['age'] = value

    def set_phone(self, value):
        self._args['phone'] = value

    def set_username(self, value):
        self._args['username'] = value

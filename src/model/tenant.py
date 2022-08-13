from src.model.model import BaseModel


class Tenant(BaseModel):
    def __init__(self, tenant_id=-1, full_name='', sex='', city='', qualities='', age=-1, solvency='None'):
        super().__init__(
            id=tenant_id,
            full_name=full_name,
            sex=sex,
            city=city,
            qualities=qualities,
            age=age,
            solvency=solvency
        )

    @property
    def id(self):
        return self._args['id']

    @property
    def full_name(self):
        return self._args['full_name']

    @property
    def sex(self):
        return self._args['sex']

    @property
    def city(self):
        return self._args['city']

    @property
    def qualities(self):
        return self._args['qualities']

    @property
    def age(self):
        return self._args['age']

    @property
    def solvency(self):
        return self._args['solvency']

    def set_id(self, value):
        self._args['id'] = value

    def set_full_name(self, value):
        self._args['full_name'] = value

    def set_sex(self, value):
        self._args['sex'] = value

    def set_city(self, value):
        self._args['city'] = value

    def set_qualities(self, value):
        self._args['qualities'] = value

    def set_age(self, value):
        self._args['value'] = value

    def set_solvency(self, value):
        self._args['solvency'] = value

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

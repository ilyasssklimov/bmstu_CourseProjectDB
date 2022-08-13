from src.model.model import BaseModel


class Neighborhood(BaseModel):
    def __init__(self, neighborhood_id=-1, tenant_id=-1, neighbors=-1, price=-1, place='', sex='', preferences=''):
        super().__init__(
            id=neighborhood_id,
            tenant_id=tenant_id,
            neighbors=neighbors,
            price=price,
            place=place,
            sex=sex,
            preferences=preferences
        )

    @property
    def id(self):
        return self._args['id']

    @property
    def tenant_id(self):
        return self._args['tenant_id']

    @property
    def neighbors(self):
        return self._args['neighbors']

    @property
    def price(self):
        return self._args['price']

    @property
    def place(self):
        return self._args['price']

    @property
    def sex(self):
        return self._args['sex']

    @property
    def preferences(self):
        return self._args['preferences']

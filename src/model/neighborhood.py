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

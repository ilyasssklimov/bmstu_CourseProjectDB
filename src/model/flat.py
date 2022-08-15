from src.model.model import BaseModel


class Flat(BaseModel):
    def __init__(self, flat_id=-1, owner_id=-1, price=-1, rooms=-1, square=-1, address='', metro='',
                 floor=-1, max_floor=-1, description=''):
        super().__init__(
            id=flat_id,
            owner_id=owner_id,
            price=price,
            rooms=rooms,
            square=square,
            address=address,
            metro=metro,
            floor=floor,
            max_floor=max_floor,
            description=description
        )

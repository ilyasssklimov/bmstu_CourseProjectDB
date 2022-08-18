from src.model.model import BaseModel


class Goods(BaseModel):
    def __init__(self, goods_id=-1, owner_id=-1, name='', price=-1, condition='', bargain=None):
        super().__init__(
            id=goods_id,
            owner_id=owner_id,
            name=name,
            price=price,
            condition=condition,
            bargain=bargain
        )

    def __eq__(self, other):
        return (
            self.id == other.id and
            self.owner_id == other.owner_id and
            self.name == other.name and
            self.price == other.price and
            self.condition == other.condition and
            ((not self.bargain and other.bargain == 'null') or
             str(self.solvency).lower() == str(other.solvency).lower())
        )


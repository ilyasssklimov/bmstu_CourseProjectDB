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

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

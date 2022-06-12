import logging
import psycopg2 as ps

from src.controller.tenant import TenantController
from src.model.flat import Flat


class LandlordController(TenantController):
    def add_flat(self, owner_id: int, price: int, square: float, address: str, metro: str,
                 floor: int, max_floor: int, description: int):
        try:
            flat = self._db.add_flat(owner_id, price, square, address, metro, floor, max_floor, description)
            return Flat(flat)
        except ps.errors.CheckViolation as e:
            logging.error(e)
            logging.error(f'Invalid params while adding flat with owner_id \'{owner_id}\'')
        return Flat()

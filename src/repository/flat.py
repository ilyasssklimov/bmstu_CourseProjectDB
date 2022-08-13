import logging
from src.database.database import BaseDatabase
from src.model.flat import Flat


class FlatRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def get_flats(self) -> list[Flat]:
        flats = [Flat(*flat) for flat in self.__db.get_flats()]
        flats.sort(key=lambda flat: flat.id)
        return flats

    def delete_flat(self, flat_id: int) -> Flat:
        try:
            del_flat = Flat(*self.__db.delete_flat(flat_id))
            return del_flat
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting flat with id = {flat_id}')

        return Flat()

    def add_flat(self, flat: Flat) -> Flat:
        try:
            add_flat = Flat(*self.__db.add_flat(*flat.get_params()[1:]))
            return add_flat
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding flat with id = {flat.id}')

        return Flat()

    def update_flat(self, flat: Flat) -> Flat:
        try:
            upd_flat = Flat(*self.__db.update_flat(*flat.get_params()))
            return upd_flat
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating flat with id = {flat.id}')

        return Flat()

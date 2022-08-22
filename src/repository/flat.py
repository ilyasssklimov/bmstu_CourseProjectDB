import logging
from multipledispatch import dispatch
from src.database.database import BaseDatabase
from src.model.flat import Flat


class FlatRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    @dispatch()
    def get_flats(self) -> list[Flat]:
        try:
            flats = [Flat(*flat) for flat in self.__db.get_flats()]
            flats.sort(key=lambda flat: flat.id, reverse=True)
            return flats
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting flats')

        return []

    @dispatch(tuple[int, int], tuple[int, int], tuple[float, float], list[str])
    def get_flats(self, price: tuple[int, int], rooms: tuple[int, int], square: tuple[float, float],
                  metro: list[str]) -> list[Flat]:
        try:
            flats = [Flat(*flat) for flat in self.__db.get_flats(price, rooms, square, metro)]
            flats.sort(key=lambda flat: flat.id, reverse=True)
            return flats
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting flats by filters')

        return []

    def delete_flat(self, flat_id: int) -> Flat:
        try:
            del_flat = Flat(*self.__db.delete_flat(flat_id))
            return del_flat
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting flat with id = {flat_id}')

        return Flat()

    def delete_flats(self) -> list[Flat]:
        try:
            del_flats = [Flat(*flat) for flat in self.__db.delete_flats()]
            return del_flats
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting flats')

        return []

    def add_flat(self, flat: Flat) -> Flat:
        try:
            new_flat = Flat(*self.__db.add_flat(*flat.get_params()[1:]))
            return new_flat
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

    def add_photo(self, flat_id: int, photo: str) -> str:
        try:
            new_photo = self.__db.add_photo(flat_id, photo)
            return new_photo
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding photo to flat with id = {flat_id}')

        return ''

    def get_photos(self, flat_id: int) -> list[str]:
        try:
            photos = self.__db.get_photos(flat_id)
            return photos
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting photos of flat with id = {flat_id}')

        return []

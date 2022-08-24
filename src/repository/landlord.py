import logging
from multipledispatch import dispatch
from src.database.database import BaseDatabase
from src.model.landlord import Landlord


class LandlordRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def get_landlords(self) -> list[Landlord]:
        try:
            landlords = [Landlord(*landlord) for landlord in self.__db.get_landlords()]
            landlords.sort(key=lambda landlord: landlord.id)
            return landlords
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting landlords')

        return []

    @dispatch(int)
    def get_landlord(self, landlord_id: int) -> Landlord:
        try:
            landlord = Landlord(*self.__db.get_landlord(landlord_id))
            return landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting landlord with id = {landlord_id}')

        return Landlord()

    @dispatch(str)
    def get_landlord(self, landlord_name: str) -> Landlord:
        try:
            landlord = Landlord(*self.__db.get_landlord(landlord_name))
            return landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting landlord with name = {landlord_name}')

        return Landlord()

    def delete_landlord(self, landlord_id: int) -> Landlord:
        try:
            del_landlord = Landlord(*self.__db.delete_landlord(landlord_id))
            return del_landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting landlord with id = {landlord_id}')

        return Landlord()

    def delete_landlords(self) -> list[Landlord]:
        try:
            del_landlords = [Landlord(*landlord) for landlord in self.__db.delete_landlords()]
            return del_landlords
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting landlords')

        return []

    def add_landlord(self, landlord: Landlord) -> Landlord:
        try:
            new_landlord = Landlord(*self.__db.add_landlord(*landlord.get_params()))
            return new_landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding landlord with name \'{landlord.full_name}\'')

        return Landlord()

    def update_landlord(self, landlord: Landlord) -> Landlord:
        try:
            upd_landlord = Landlord(*self.__db.update_landlord(*landlord.get_params()))
            return upd_landlord
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating landlord with name \'{landlord.full_name}\'')

        return Landlord()

    def check_landlord(self, landlord_id: int) -> bool:
        logging.info(f'Checking landlord with id = {landlord_id}')
        return self.__db.check_landlord(landlord_id)

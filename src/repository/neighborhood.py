import logging
from src.database.database import BaseDatabase
from src.model.neighborhood import Neighborhood


class NeighborhoodRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def get_neighborhoods(self) -> list[Neighborhood]:
        try:
            neighborhoods = [Neighborhood(*neighborhood) for neighborhood in self.__db.get_neighborhoods()]
            neighborhoods.sort(key=lambda neighborhood: neighborhood.id, reverse=True)
            return neighborhoods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting neighborhoods')

        return []

    def delete_neighborhood(self, neighborhood_id: int) -> Neighborhood:
        try:
            del_neighborhood = Neighborhood(*self.__db.delete_neighborhood(neighborhood_id))
            return del_neighborhood
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting neighborhood with id = {neighborhood_id}')

        return Neighborhood()

    def delete_neighborhoods(self) -> list[Neighborhood]:
        try:
            del_neighborhoods = [Neighborhood(neighborhood) for neighborhood in self.__db.delete_neighborhoods()]
            return del_neighborhoods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting neighborhoods')

        return []

    def add_neighborhood(self, neighborhood: Neighborhood) -> Neighborhood:
        try:
            new_neighborhood = Neighborhood(*self.__db.add_neighborhood(*neighborhood.get_params()[1:]))
            return new_neighborhood
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding neighborhood with tenant_id = {neighborhood.tenant_id}')

        return Neighborhood()

    def update_neighborhood(self, neighborhood: Neighborhood) -> Neighborhood:
        try:
            upd_neighborhood = Neighborhood(*self.__db.update_neighborhood(*neighborhood.get_params()))
            return upd_neighborhood
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating neighborhood with tenant_id = {neighborhood.tenant_id}')

        return Neighborhood()

import logging
from multipledispatch import dispatch
from src.database.database import BaseDatabase
from src.model.goods import Goods


class GoodsRepository:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def get_goods(self) -> list[Goods]:
        try:
            goods = [Goods(*goods) for goods in self.__db.get_goods()]
            goods.sort(key=lambda g: g.id, reverse=True)
            return goods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while getting goods')

        return []

    @dispatch(int)
    def delete_goods(self, goods_id: int) -> Goods:
        try:
            del_goods = Goods(*self.__db.delete_goods(goods_id))
            return del_goods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting goods with id = {goods_id}')

        return Goods()

    @dispatch()
    def delete_goods(self) -> list[Goods]:
        try:
            del_goods = [Goods(*goods) for goods in self.__db.delete_goods()]
            return del_goods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while deleting goods')

        return []

    def add_goods(self, goods: Goods) -> Goods:
        try:
            new_goods = Goods(*self.__db.add_goods(*goods.get_params()[1:]))
            return new_goods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while adding goods with owner_id = {goods.owner_id}')

        return Goods()

    def update_goods(self, goods: Goods) -> Goods:
        try:
            upd_goods = Goods(*self.__db.update_goods(*goods.get_params()))
            return upd_goods
        except Exception as e:
            logging.error(e)
            logging.error(f'Some error while updating goods with id = {goods.id}')

        return Goods()

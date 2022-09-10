from src.index_test.config import REPEAT_TIMES
from src.database.database import BaseDatabase


class AnalyzeQuery:
    def __init__(self, db: BaseDatabase):
        self.__db = db

    def __del__(self):
        self.__db.disconnect_db()

    def drop_index(self, name: str):
        query = f'''DROP INDEX IF EXISTS {name}'''
        self.__db.execute(query)

    def create_index(self, name: str, table: str, column: str):
        query = f'''CREATE INDEX {name} ON {table} ({column})'''
        self.__db.execute(query)

    def __get_time(self, table: str, field: str, owner_id: int) -> float:
        query = f'''EXPLAIN ANALYZE SELECT * FROM public.{table} where {field} = {owner_id}'''
        return float(self.__db.select(query)[-1][0].split()[-2])

    def __loop_count(self, table: str, field: str, owner_id: int) -> float:
        result = 0.0
        for _ in range(REPEAT_TIMES):
            result += self.__get_time(table, field, owner_id)
        result /= REPEAT_TIMES
        return result

    def analyze_query(self, table: str, field: str, owner_id: int, index: bool = False) -> float:
        self.drop_index(f'{table}_index')
        if index:
            self.create_index(f'{table}_index', f'public.{table}', field)

        result = self.__loop_count(table, field, owner_id)
        return round(result, 6)

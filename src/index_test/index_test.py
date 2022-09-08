from prettytable import PrettyTable
import sys
sys.path.append('.')

from src.index_test.analyze import AnalyzeQuery
from src.database.config import DB_DEFAULT_PARAMS
from src.database.pg_database import PgDatabase


def main():
    user_id = 5469717692
    table = PrettyTable()
    table.field_names = ['Таблица', 'Время без индекса', 'Время с индексом']

    database = PgDatabase(DB_DEFAULT_PARAMS)
    analyzer = AnalyzeQuery(database)

    without_index = [
        analyzer.analyze_query('flat', 'owner_id', user_id),
        analyzer.analyze_query('neighborhood', 'tenant_id', user_id),
        analyzer.analyze_query('goods', 'owner_id', user_id)
    ]

    with_index = [
        analyzer.analyze_query('flat', 'owner_id', user_id, index=True),
        analyzer.analyze_query('neighborhood', 'tenant_id', user_id, index=True),
        analyzer.analyze_query('goods', 'owner_id', user_id, index=True)
    ]

    table.add_row(['Квартиры', without_index[0], with_index[0]])
    table.add_row(['Соседство', without_index[1], with_index[1]])
    table.add_row(['Товары', without_index[2], with_index[2]])

    print(table)


if __name__ == '__main__':
    main()

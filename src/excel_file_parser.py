"""Use 'python excel_file_parser.py' command to run this script"""
from datetime import datetime
from libs.database import Database
from libs.data_processor import DataProcessor
from libs.excel_parser import ExcelParser
from libs.table_formatter import TableFormatter


if __name__ == '__main__':
    file_parser = ExcelParser(filename='file.xlsx')
    data_rows = file_parser.parse_worksheet()

    sqlite_db = Database('sqlite_python.db')
    sqlite_db.__enter__()
    sqlite_db.create_table()

    data_processor = DataProcessor(data_rows)
    data_processor.process_data(storage=sqlite_db)

    results = sqlite_db.select_total_data()

    table_headers = [description[0] for description in sqlite_db.cursor.description]
    table_formatter = TableFormatter(table_headers)
    for row in results:
        # row structure example: (1682629200, 'company1', 'forecast', 88, 180)
        date = datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d')
        table_formatter.add_row([date, row[1], row[2], row[3], row[4]])
    table_formatter.show()

    sqlite_db.close()

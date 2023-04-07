"""Use 'python excel_parser.py' command to run this script"""
import sqlite3
from datetime import datetime
import random
from openpyxl import load_workbook
from prettytable import PrettyTable


COLUMNS_NAMES_STR = ("(id, "
                    "company, "
                    "factQliqdata1, "
                    "factQliqdata2, "
                    "factQoildata1, "
                    "factQoildata2, "
                    "forecastQliqdata1, "
                    "forecastQliqdata2, "
                    "forecastQoildata1, "
                    "forecastQoildata2, "
                    "date)")
YEAR = 2023
MONTH = 4


workbook = load_workbook(filename='file.xlsx')
worksheet = workbook.active

sqlite_connection = sqlite3.connect('sqlite_python.db')
cursor = sqlite_connection.cursor()

CREATE_TABLE_QUERY = '''CREATE TABLE IF NOT EXISTS excel_data (
                        id INTEGER PRIMARY KEY,
                        company TEXT NOT NULL,
                        factQliqdata1 INTEGER NOT NULL,
                        factQliqdata2 INTEGER NOT NULL,
                        factQoildata1 INTEGER NOT NULL,
                        factQoildata2 INTEGER NOT NULL,
                        forecastQliqdata1 INTEGER NOT NULL,
                        forecastQliqdata2 INTEGER NOT NULL,
                        forecastQoildata1 INTEGER NOT NULL,
                        forecastQoildata2 INTEGER NOT NULL,
                        date INTEGER NOT NULL);'''
cursor.execute(CREATE_TABLE_QUERY)
sqlite_connection.commit()

for row in worksheet.iter_rows(min_row=4, values_only=True):
    date = datetime(YEAR, MONTH, random.randint(1, 30))
    timestamp = int(date.timestamp())

    values = row[0:10] + (timestamp,)
    insert_query = f"""INSERT INTO excel_data {COLUMNS_NAMES_STR} VALUES {values}"""
    try:
        cursor.execute(insert_query)
    except sqlite3.IntegrityError:
        # this data already in table, ignore it
        pass

# value_type may be values 'fact' or 'forecast'
SELECT_TOTAL_QUERY = '''
                    SELECT date, company, value_type,
                        SUM(factQliqdata1 + factQliqdata2) AS TotalQliq,
                        SUM(factQoildata1 + factQoildata2) AS TotalQoil
                    FROM (
                        SELECT date, company, 'fact' AS value_type,
                            factQliqdata1, factQliqdata2, factQoildata1, factQoildata2
                        FROM excel_data
                        UNION ALL
                        SELECT date, company, 'forecast' AS value_type,
                            forecastQliqdata1, forecastQliqdata2, forecastQoildata1, forecastQoildata2
                        FROM excel_data
                    )
                    GROUP BY date, company, value_type
                    '''
cursor.execute(SELECT_TOTAL_QUERY)
results = cursor.fetchall()

table = PrettyTable()
table.field_names = [description[0] for description in cursor.description]

for row in results:
    # row structure example: (1682629200, 'company1', 'forecast', 88, 180)
    date = datetime.fromtimestamp(row[0]).strftime('%Y-%m-%d')
    table.add_row([date, row[1], row[2], row[3], row[4]])
print(table)

sqlite_connection.commit()
cursor.close()
sqlite_connection.close()

import sqlite3


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


class Database:
    """Class for managing SQLIte database"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def close(self):
        self.cursor.close()
        self.connection.close()

    def create_table(self):
        create_table_query = '''CREATE TABLE IF NOT EXISTS excel_data (
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
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data(self, values):
        insert_query = f"""INSERT INTO excel_data {COLUMNS_NAMES_STR} VALUES {values}"""
        try:
            self.cursor.execute(insert_query)
        except sqlite3.IntegrityError:
            # this data already in table, ignore it
            pass
        self.connection.commit()

    def select_total_data(self):
        select_total_query = '''
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
        self.cursor.execute(select_total_query)
        results = self.cursor.fetchall()
        return results
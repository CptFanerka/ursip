import random
from datetime import datetime

YEAR = 2023
MONTH = 4


class DataProcessor:
    """Class for appending date to Excel data"""
    def __init__(self, data_rows):
        self.data_rows = data_rows

    def process_data(self, storage):
        for row in self.data_rows:
            date = datetime(YEAR, MONTH, random.randint(1, 30))
            timestamp = int(date.timestamp())
            data = row[0:10] + (timestamp,)
            storage.insert_data(data)
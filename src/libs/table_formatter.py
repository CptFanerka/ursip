from prettytable import PrettyTable


class TableFormatter:
    """Class for pretty printing of result table"""
    def __init__(self, headers):
        self.table = PrettyTable()
        self.table.field_names = headers

    def add_row(self, row):
        self.table.add_row(row)

    def show(self):
        print(self.table)
from os import path
from pandas import read_csv, DataFrame

class CsvToDf:
    
    def to_df(self, csv_file_name: str) -> DataFrame:
        csv_path = path.join(path.dirname(__file__), "..", "..", "storage", csv_file_name)
        return read_csv(csv_path, sep=";", encoding="utf-8")

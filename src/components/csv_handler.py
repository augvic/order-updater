from os import path
import sys
from pandas import read_csv, DataFrame

class CsvHandler:
    
    def __init__(self) -> None:
        if getattr(sys, 'frozen', False):
            self.base_path = path.dirname(sys.executable)
        else:
            self.base_path = path.join(path.dirname(__file__), "..", "..")
    
    def save_order_modified(self, order: str) -> None:
        csv_path = path.abspath(path.join(self.base_path, "storage", "orders_modified.csv"))
        with open(csv_path, "a") as file:
            file.write(order + "\n")
    
    def to_df(self, csv_file_name: str) -> DataFrame:
        csv_path = path.abspath(path.join(self.base_path, "storage", csv_file_name))
        return read_csv(csv_path, sep=";", encoding="utf-8")

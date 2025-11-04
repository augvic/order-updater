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
        try:
            csv_path = path.abspath(path.join(self.base_path, "storage", "orders_modified.csv"))
            with open(csv_path, "a") as file:
                file.write(order + "\n")
        except Exception as error:
            raise Exception(f"Error in (CsvHandler) component in (save_order_modified) method: {error}.")
    
    def to_df(self, csv_file_name: str) -> DataFrame:
        try:
            csv_path = path.abspath(path.join(self.base_path, "storage", csv_file_name))
            return read_csv(csv_path, sep=";", encoding="utf-8")
        except Exception as error:
            raise Exception(f"Error in (CsvHandler) component in (to_df) method: {error}.")

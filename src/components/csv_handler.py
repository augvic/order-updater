from os import path
import sys

class CsvHandler:
    
    def save_order_modified(self, order: str) -> None:
        if getattr(sys, 'frozen', False):
            base_path = path.dirname(sys.executable)
        else:
            base_path = path.join(path.dirname(__file__), "..", "..")
        csv_path = path.abspath(path.join(base_path, "storage", "orders_modified.csv"))
        with open(csv_path, "a") as file:
            file.write(order + "\n")

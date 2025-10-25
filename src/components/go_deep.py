from os import getenv
from dotenv import load_dotenv
from os import path
from requests import Session
import sys
import urllib3
from urllib3.exceptions import InsecureRequestWarning

class GoDeep:

    def login(self) -> None:
        urllib3.disable_warnings(InsecureRequestWarning)
        base_path: str = getattr(sys, "_MEIPASS", path.join(path.dirname(__file__), "..", ".."))
        dotenv_path =  path.abspath(path.join(base_path, ".env"))
        load_dotenv(dotenv_path)
        self.session = Session()
        self.payload = {
            "username": getenv("GODEEP_EMAIL"),
            "password": getenv("GODEEP_PASSWORD"),
            "token": ""
        }
        self.session.post("https://positivo-pme.f1b2b.com.br/admin", data=self.payload, verify=False)
        
    def export_orders_to_csv(self) -> None:
        if getattr(sys, 'frozen', False):
            base_path = path.dirname(sys.executable)
        else:
            base_path = path.join(path.dirname(__file__), "..", "..")
        destiny = path.abspath(path.join(base_path, "storage", "orders.csv"))
        response = self.session.get("https://positivo-pme.f1b2b.com.br/admin/orders/export-csv", verify=False)
        with open(destiny, "wb") as file:
            file.write(response.content)

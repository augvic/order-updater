from os import getenv
from dotenv import load_dotenv
from os import path
from requests import Session

class GoDeep:

    def login(self) -> None:
        load_dotenv()
        self.session = Session()
        self.payload = {
            "username": getenv("GODEEP_EMAIL"),
            "password": getenv("GODEEP_PASSWORD"),
            "token": ""
        }
        self.session.post("https://positivo-pme.f1b2b.com.br/admin", data=self.payload, verify=False)
        
    def export_orders_to_csv(self) -> None:
        destiny = path.abspath(path.join(path.dirname(__file__), "..", "..", "storage", ".orders.csv"))
        response = self.session.get("https://positivo-pme.f1b2b.com.br/admin/orders/export-csv", verify=False)
        with open(destiny, "wb") as file:
            file.write(response.content)

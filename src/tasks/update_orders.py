from src.components.go_deep import GoDeep
from sys import exit

class UpdateOrders:
    
    def _setup(self) -> None:
        self.go_deep_browser = GoDeep()
    
    def execute(self) -> None:
        self._setup()
        try:
            self.go_deep_browser.login()
            self.go_deep_browser.export_orders_to_csv()
        except Exception as error:
            print(f"Ocorreu um erro no componente GoDeepBrowser: {error}")
            exit()

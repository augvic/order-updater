from src.tasks.update_orders import UpdateOrders
import time

class Cli:
    
    def __init__(self) -> None:
        try:
            update_orders_task = UpdateOrders()
            while True:
                update_orders_task.execute()
                print("")
                print('⏳ Aguardando 30m para reinício.')
                time.sleep(1800)
                print("")
        except Exception as error:
            print(error)

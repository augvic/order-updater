from src.tasks.update_orders import UpdateOrders

class Cli:
    
    def __init__(self) -> None:
        update_orders_task = UpdateOrders()
        while True:
            try:
                update_orders_task.execute()
            except Exception as error:
                print(error)
            response = input('❗ Para reiniciar aperte ENTER. Para sair digite "SAIR": ')
            if response == "SAIR":
                break
            print("")

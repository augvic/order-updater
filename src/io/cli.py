from src.tasks.update_orders import UpdateOrders

class Cli:
    
    def __init__(self) -> None:
        try:
            update_orders_task = UpdateOrders()
            while True:
                update_orders_task.execute()
                response = input('❗ Para reiniciar aperte ENTER. Para sair digite "SAIR": ')
                if response == "SAIR":
                    break
                print("")
        except Exception as error:
            print(error)

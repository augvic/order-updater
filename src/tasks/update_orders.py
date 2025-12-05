from src.components.go_deep import GoDeep
from src.components.sap_client import SapClient
from src.components.csv_handler import CsvHandler
from datetime import datetime

class UpdateOrders:
    
    def __init__(self) -> None:
        self.go_deep = GoDeep()
        self.sap_client = SapClient()
        self.csv_handler = CsvHandler()
    
    def execute(self) -> None:
        try:
            print(f"⌚ <{datetime.now().replace(microsecond=0).strftime("%d/%m/%Y %H:%M:%S")}>")
            print("Iniciando execução.")
            print("📩 Extraindo CSV dos pedidos...")
            self.go_deep.login()
            self.go_deep.export_orders_to_csv()
            print("✅ Concluído.")
            print("🛠️ Montando DataFrames...")
            sellers_df = self.csv_handler.to_df("sellers.csv")
            orders_df = self.csv_handler.to_df("orders.csv")
            orders_df_columns_used = orders_df[["ERP Codigo Pedido", "Nome do usuário", "Status"]]
            orders_df_filtered = orders_df_columns_used[orders_df_columns_used["ERP Codigo Pedido"].notna() & orders_df_columns_used["Nome do usuário"].isin(sellers_df["Seller Name"]) & orders_df_columns_used["Status"].isin(["Pedido integrado", "Pagamento aprovado", "Em separação"])].copy()
            orders_modified_df = self.csv_handler.to_df("orders_modified.csv")
            orders_modified = orders_modified_df["Orders Modified"].astype(str).to_list()
            print("✅ Concluído.")
            print("♾️ Criando ligação com SAP...")
            self.sap_client.init()
            print("✅ Concluído.")
            print("🔄 Atualizando ordens...")
            for _, order_df_row in orders_df_filtered.iterrows():
                orders = order_df_row["ERP Codigo Pedido"]
                orders = str(orders).split("|")
                for order in orders:
                    order = str(int(float(order)))
                    if order not in orders_modified:
                        seller_df_row = sellers_df[sellers_df["Seller Name"] == order_df_row["Nome do usuário"]].iloc[0]
                        self.sap_client.update_order(order, seller_df_row["Partner Code"], seller_df_row["Comission Code"])
                        self.csv_handler.save_order_modified(order)
            self.sap_client.go_home()
            print("✅ Concluído.")
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro durante a execução da tarefa: {error}.")

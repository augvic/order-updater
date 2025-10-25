from src.components.go_deep import GoDeep
from src.components.sap_client import SapClient
from src.components.csv_handler import CsvHandler
from datetime import datetime

class UpdateOrders:
    
    def _setup(self) -> None:
        self.go_deep = GoDeep()
        self.sap_client = SapClient()
        self.csv_handler = CsvHandler()
    
    def execute(self) -> None:
        self._setup()
        print(f"⌚ <{datetime.now().replace(microsecond=0).strftime("%d/%m/%Y %H:%M:%S")}>")
        print("Iniciando execução.")
        try:
            print("📩 Extraindo CSV dos pedidos...")
            self.go_deep.login()
            self.go_deep.export_orders_to_csv()
            print("✅ Concluído.")
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro no componente GoDeep: {error}")
        print("🛠️ Montando DataFrames...")
        try:
            sellers_df = self.csv_handler.to_df("sellers.csv")
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro gerar DataFrame dos vendedores: {error}")
        try:
            orders_df = self.csv_handler.to_df("orders.csv")
            orders_df_columns_used = orders_df[["ERP Codigo Pedido", "Nome do usuário", "Status"]]
            orders_df_filtered = orders_df_columns_used[orders_df_columns_used["ERP Codigo Pedido"].notna() & orders_df_columns_used["Nome do usuário"].isin(sellers_df["Seller Name"]) & orders_df_columns_used["Status"].isin(["Pedido integrado", "Pagamento aprovado", "Em separação"])]
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro gerar DataFrame das ordens: {error}")
        try:
            orders_modified_df = self.csv_handler.to_df("orders_modified.csv")
            orders_modified = orders_modified_df["Orders Modified"].astype(str).to_list()
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro gerar DataFrame das ordens modificadas: {error}")
        print("✅ Concluído.")
        try:
            print("♾️ Criando ligação com SAP...")
            self.sap_client.init()
        except Exception as error:
            raise Exception(f"❌ Ocorreu um erro no componente SapClient: {error}")
        print("✅ Concluído.")
        print("🔄 Atualizando ordens...")
        for _, order_df_row in orders_df_filtered.iterrows():
            order = order_df_row["ERP Codigo Pedido"]
            if order not in orders_modified:
                seller_df_row = sellers_df[sellers_df["Seller Name"] == order_df_row["Nome do usuário"]].iloc[0]
                try:
                    self.sap_client.update_order(order_df_row["ERP Codigo Pedido"], seller_df_row["Partner Code"], seller_df_row["Comission Code"])
                except Exception as error:
                    raise Exception(f"❌ Ocorreu um erro ao atualizar ordem: {error}")
                try:
                    self.csv_handler.save_order_modified(order_df_row["ERP Codigo Pedido"])
                except Exception as error:
                    raise Exception(f"❌ Ocorreu um erro no componente CsvHandler: {error}")
        self.sap_client.go_home()
        print("✅ Concluído.")

from pandas import read_csv
from os import path

sellers_csv_path = path.join(path.dirname(__file__), "..", "storage", ".sellers.csv")
sellers_df = read_csv(sellers_csv_path, sep=";", encoding="utf-8")
orders_csv_path = path.join(path.dirname(__file__), "..", "storage", ".orders.csv")
orders_df = read_csv(orders_csv_path, sep=";", encoding="utf-8")
orders_df_columns_used = orders_df[["ERP Codigo Pedido", "Nome do usuário", "Status"]]
orders_df_filtered = orders_df_columns_used[orders_df_columns_used["ERP Codigo Pedido"].notna() & orders_df_columns_used["Nome do usuário"].isin(sellers_df["Seller Name"]) & orders_df_columns_used["Status"].isin(["Pedido integrado", "Pagamento aprovado"])]
for _, order_df_row in orders_df_filtered.iterrows():
    seller_df_row = sellers_df[sellers_df["Seller Name"] == order_df_row["Nome do usuário"]].iloc[0]
    print(f"Ordem: {order_df_row["ERP Codigo Pedido"]}, Parceiro: {seller_df_row["Partner Code"]}, Comissão: {seller_df_row["Comission Code"]}")

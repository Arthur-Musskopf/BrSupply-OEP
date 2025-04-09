# src/tools/tool_merge_dfs.py
from langchain.tools import tool

@tool
def merge_pedidos_info(pedido_id: str) -> str:
    """
    Retorna informações do pedido correlacionadas com tracking, usuário e contestações.
    """
    from src.load_data import obter_dataframes
    dfs = obter_dataframes()

    try:
        df = dfs["pedidos_detalhados"]
        tracking = dfs["tracking"]
        usuarios = dfs["usuarios"]
        cont = dfs["contestacoes"]

        df_merged = df[df["Pedido"] == pedido_id] \
            .merge(tracking, on="Pedido", how="left") \
            .merge(usuarios, on="Login", how="left") \
            .merge(cont, on="Pedido", how="left")

        if df_merged.empty:
            return f"Não foi encontrado o pedido {pedido_id}."
        else:
            return df_merged.iloc[0].to_string()
    except Exception as e:
        return f"Ocorreu um erro: {e}"

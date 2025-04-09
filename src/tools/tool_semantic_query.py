from langchain.tools import tool
from src.load_data import obter_dataframes
import pandas as pd

@tool
def tool_consulta_semantica(query: str) -> str:
    '''
    Consulta cruzada entre tabelas do sistema Supply Manager do IFMT.
    A tool analisa a intenção do usuário e tenta responder por meio de filtros, agregações e joins semânticos.
    Ex: 'Qual o valor total dos pedidos em março?', 'Quem aprovou mais pedidos?', 'Qual o item mais vendido?'
    '''

    dfs = obter_dataframes()
    try:
        pedidos = dfs.get("pedidos_detalhados")
        if pedidos is None or pedidos.empty:
            return "A base de pedidos não está disponível."

        # Padronizar colunas
        pedidos["Data Pedido"] = pd.to_datetime(pedidos["Data Pedido"], errors="coerce")
        pedidos["Valor Total"] = (
            pedidos["Valor Total"]
            .astype(str)
            .str.replace("R$", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        if "março" in query and "quantos pedidos" in query:
            pedidos_marco = pedidos[pedidos["Data Pedido"].dt.month == 3]
            return f"Foram feitos {len(pedidos_marco)} pedidos em março."

        if "valor total" in query and "março" in query:
            pedidos_marco = pedidos[pedidos["Data Pedido"].dt.month == 3]
            total = pedidos_marco["Valor Total"].sum()
            return f"O valor total dos pedidos em março é R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        if "item mais vendido" in query and "valor" in query:
            item = pedidos.groupby("Nome do Item")["Valor Total"].sum().idxmax()
            val = pedidos.groupby("Nome do Item")["Valor Total"].sum().max()
            return f"O item com maior valor de venda é '{item}', totalizando R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        if "item mais vendido" in query and "quantidade" in query or "mais comprado" in query:
            item = pedidos.groupby("Nome do Item")["Quant."].sum().idxmax()
            qtd = pedidos.groupby("Nome do Item")["Quant."].sum().max()
            return f"O item mais comprado foi '{item}', com {int(qtd)} unidades."

        return "Não consegui interpretar a consulta. Tente reformular com termos como 'valor total', 'quantos', 'item mais vendido', 'março', etc."
    except Exception as e:
        return f"Ocorreu um erro durante a análise semântica: {e}"
# src/tools/tool_max_min_valores.py
from langchain.tools import tool

@tool
def consulta_max_min(coluna: str = "Valor Total", tipo: str = "max") -> str:
    """
    Retorna o maior ou menor valor da coluna especificada dos pedidos.
    Parâmetros:
    - coluna: nome da coluna (ex: "Valor Total")
    - tipo: "max" ou "min"
    """
    import pandas as pd
    from src.load_data import obter_dataframes

    df = obter_dataframes()["pedidos_detalhados"].copy()
    df[coluna] = df[coluna].replace({'R\$': '', ',': '.'}, regex=True).astype(float)

    if tipo == "max":
        valor = df[coluna].max()
    else:
        valor = df[coluna].min()

    return f"O valor {tipo} da coluna '{coluna}' é R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

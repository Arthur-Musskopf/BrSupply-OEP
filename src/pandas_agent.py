from langchain_experimental.agents import create_pandas_dataframe_agent

def construir_pandas_agent(llm, dfs):
    return create_pandas_dataframe_agent(
        llm=llm,
        df=dfs["pedidos_detalhados"],  # ou outro df
        verbose=True,
        allow_dangerous_code=True
    )

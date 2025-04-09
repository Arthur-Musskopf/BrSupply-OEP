from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.prompts import ChatPromptTemplate
from langchain.agents.agent_types import AgentType

from src.tools.tool_max_min_valores import consulta_max_min
from src.tools.tool_merge_dfs import merge_pedidos_info
from src.tools.usuario_logado_tool import criar_tool_info_usuario_logado
from src.prompts.analise_dados_prompt import get_prompt_analise_dados

def construir_pandas_agent(llm, dfs, login_usuario: str):
    login_usuario = str(login_usuario).strip()
    prompt = get_prompt_analise_dados()
    info_usuario_tool = criar_tool_info_usuario_logado(login_usuario)

    return create_pandas_dataframe_agent(
        llm=llm,
        df=dfs["pedidos_detalhados"],
        tools=[consulta_max_min, merge_pedidos_info, info_usuario_tool],
        prompt=prompt,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        handle_parsing_errors=True,
        return_intermediate_steps=False,
        allow_dangerous_code=True
    )
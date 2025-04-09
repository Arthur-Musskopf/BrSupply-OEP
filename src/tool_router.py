from src.intent_classifier import classificar_intencao
from langchain_core.tools import Tool

def rotear_para_tool(pergunta: str, ferramentas: list[Tool]) -> str | None:
    """
    Recebe a pergunta e tenta rotear para a tool mais adequada com base na intenção detectada.
    Retorna o resultado se uma tool for invocada diretamente, ou None para fallback.
    """
    intencao = classificar_intencao(pergunta)
    
    tool_map = {
        "perfil_usuario": "info_usuario_logado",
        "analitica_semantica": "tool_consulta_semantica",
        "rastreamento": "merge_pedidos_info"
    }

    if intencao in tool_map:
        nome_tool = tool_map[intencao]
        for tool in ferramentas:
            if tool.name == nome_tool:
                return tool.invoke(pergunta)
    
    return None  # Deixa o agente decidir
# src/tools/usuario_logado_tool.py
from langchain.tools import Tool
from functools import partial
from src.load_data import obter_dataframes

def _buscar_info_usuario(login: str) -> str:
    """
    Retorna nome e dados do usuário logado a partir do CPF.
    """
    usuarios = obter_dataframes()["usuarios"]
    user = usuarios[usuarios["Login"].astype(str).str.zfill(11) == login]
    if not user.empty:
        dados = user.iloc[0]
        return f"Usuário: {dados['Nome']} | CPF: {dados['Login']} | Email: {dados.get('Email', 'não informado')}"
    else:
        return "Usuário não encontrado."

def criar_tool_info_usuario_logado(login: str) -> Tool:
    return Tool.from_function(
        func=partial(_buscar_info_usuario, login),
        name="info_usuario_logado",
        description="Retorna os dados do usuário logado no sistema a partir do CPF usado no login."
    )

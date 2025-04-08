import os
import csv
import json
from datetime import datetime
from typing import Optional, List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

LOG_DIR = "data/processed/logs"
CSV_LOG = os.path.join(LOG_DIR, "logs.csv")
JSONL_LOG = os.path.join(LOG_DIR, "logs.jsonl")
os.makedirs(LOG_DIR, exist_ok=True)


# 🟢 1. INÍCIO DE SESSÃO
def iniciar_sessao(usuario: str) -> dict:
    return {
        "usuario": usuario,
        "inicio": datetime.now(),
        "historico": [],
        "escalonamento_humano": False,
        "tipo_pergunta": None,
        "status": "em_execucao",
    }


# 🟡 2. GERA RESUMO COM LLM
def gerar_resumo_conversa(llm, historico: List[dict]) -> str:
    template = """
Você é um assistente que resume conversas entre usuários e um agente de atendimento.

Histórico da conversa:
{mensagens}

Resumo:"""
    prompt = PromptTemplate(input_variables=["mensagens"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)

    mensagens_formatadas = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in historico]
    )
    return chain.run({"mensagens": mensagens_formatadas}).strip()


# 🔴 3. ENCERRAMENTO E LOGGING
def encerrar_sessao(sessao: dict, llm, tipo_pergunta: str, sucesso=True):
    fim = datetime.now()
    sessao["fim"] = fim
    sessao["duracao_segundos"] = round((fim - sessao["inicio"]).total_seconds())
    sessao["tipo_pergunta"] = tipo_pergunta
    sessao["status"] = (
        "finalizado_sucesso" if sucesso else
        "humano_escalonado" if sessao["escalonamento_humano"]
        else "finalizado_erro"
    )

    try:
        sessao["resumo"] = gerar_resumo_conversa(llm, sessao["historico"])
    except Exception as e:
        sessao["resumo"] = f"[Erro ao gerar resumo automático]: {e}"

    salvar_log(sessao)


# 💾 4. SALVAR LOG (csv + jsonl)
def salvar_log(sessao: dict):
    campos_csv = [
        "usuario", "inicio", "fim", "duracao_segundos",
        "tipo_pergunta", "escalonamento_humano", "resumo", "status"
    ]

    # CSV
    with open(CSV_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos_csv)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow({
            k: sessao.get(k) if not isinstance(sessao.get(k), datetime)
            else sessao[k].isoformat()
            for k in campos_csv
        })

    # JSONL
    json_copy = dict(sessao)
    for k in ["inicio", "fim"]:
        if isinstance(json_copy.get(k), datetime):
            json_copy[k] = json_copy[k].isoformat()
    with open(JSONL_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(json_copy, ensure_ascii=False) + "\n")

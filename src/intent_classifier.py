def classificar_intencao(texto: str) -> str:
    texto = texto.lower()
    if any(p in texto for p in ["falar com", "quero atendimento", "responsável"]):
        return "escalonamento"
    elif any(p in texto for p in ["quantos", "qual o valor", "agrupado", "total", "soma", "média"]):
        return "analitica"
    return "informativa"

def classificar_intencao(texto: str) -> str:
    texto = texto.lower()

    if any(p in texto for p in ["falar com", "quero atendimento", "responsável", "ajuda humana", "preciso falar com alguém"]):
        return "escalonamento"

    elif any(p in texto for p in [
        "quantos", "qual o valor", "agrupado", "total", "soma", "média", 
        "item mais comprado", "valor total", "contagem", "média por mês",
        "maior valor", "menor valor", "mais vendido", "mais comprado"
    ]):
        return "analitica_semantica"

    elif any(p in texto for p in ["quem sou eu", "meus dados", "meu perfil", "dados do login", "identidade"]):
        return "perfil_usuario"

    elif any(p in texto for p in [
        "pedido entregue", "entregues", "rastreamento", "tracking", 
        "não chegou", "ainda não entregaram", "status do pedido", "em trânsito"
    ]):
        return "rastreamento"

    elif any(p in texto for p in [
        "como criar usuário", "novo usuário", "cadastrar solicitante", "inserir aprovador", "criação de conta"
    ]):
        return "informativa_criacao_usuarios"

    elif any(p in texto for p in [
        "como aprovar", "fluxo de aprovação", "reprovar pedido", "etapas de aprovação"
    ]):
        return "informativa_fluxo_aprovacao"

    return "informativa"
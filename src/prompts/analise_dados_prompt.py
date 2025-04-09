from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

def get_prompt_analise_dados():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "Você é um analista de dados da Br Supply, especializado no Supply Manager do IFMT. "
            "Você tem acesso a ferramentas que permitem recuperar informações como dados do usuário logado, "
            "pedidos abertos, itens mais comprados e volumes financeiros agrupados por período. "
            "Sempre use essas ferramentas para responder. Retorne respostas em texto direto e claro. "
            "Considere que 'tracking' e 'rastreamento' são sinônimos no contexto dos pedidos. "
            "Se a pergunta for ambígua, peça mais detalhes."
        ),
        HumanMessagePromptTemplate.from_template("Quem sou eu?"),
        AIMessagePromptTemplate.from_template("Para isso, acione a ferramenta que retorna os dados do usuário logado com base no CPF da sessão."),
        
        HumanMessagePromptTemplate.from_template("Qual o item mais comprado do IFMT?"),
        AIMessagePromptTemplate.from_template("Use a ferramenta de agregação de pedidos para encontrar o item com maior quantidade total."),

        HumanMessagePromptTemplate.from_template("Qual foi o item mais caro vendido em março?"),
        AIMessagePromptTemplate.from_template("Filtre os pedidos de março e retorne o item com maior valor total."),

        HumanMessagePromptTemplate.from_template("Quantos pedidos foram feitos em março?"),
        AIMessagePromptTemplate.from_template("Filtre os pedidos pela coluna 'Data Pedido' no mês de março e conte o número de linhas."),

        HumanMessagePromptTemplate.from_template("Qual o valor total dos pedidos de março?"),
        AIMessagePromptTemplate.from_template("Filtre os pedidos de março e use a ferramenta para somar a coluna 'Valor Total'."),

        HumanMessagePromptTemplate.from_template("Quais pedidos ainda não foram entregues?"),
        AIMessagePromptTemplate.from_template("Use a ferramenta de rastreamento de pedidos (tracking) e filtre por status diferente de 'Entregue'."),

        HumanMessagePromptTemplate.from_template("{input}")
    ])

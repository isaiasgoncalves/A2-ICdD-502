"""MÓDULO DE CONEXÃO COM OPENAI PARA ANALISE DAS AVALIAÇÕES"""

from openai import OpenAI
import json

# Inicializa o cliente da OpenAI com a sua chave API
client = OpenAI(api_key='coloque a chave aqui')

# Função que contabiliza os tópicos identificados nas avaliações
def contabiliza_topico(topicos, contagem_positivos, contagem_negativos):
    for topico in topicos:
        if topico in contagem_positivos:
            contagem_positivos[topico] += 1
        elif topico in contagem_negativos:
            contagem_negativos[topico] += 1

# Define a ferramenta para chamada de funções com OpenAI
tools = [{
    "type": "function",
    "function": {
        "name": "contabiliza_topico",
        "description": "Adiciona os tópicos da avaliação na contagem geral",
        "parameters": {
            "type": "object",
            "properties": {
                "topicos": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["topicos"],
        },
    },
}]

# Mapeia a função disponível para uso pelo sistema
funcoes_disponiveis = {"contabiliza_topico": contabiliza_topico}

# Define os tópicos positivos e negativos que serão procurados nas avaliações
topicos_positivos = [
    "Ótimo serviço",
    "Entrega rápida",
    "Atendimento excelente",
    "Qualidade do produto",
    "Recomendo",
    "Embalagem de qualidade",
    "Eficiência no serviço de entrega",
    "Serviço de qualidade",
    "Velocidade no serviço",
    "Superou expectativas",
    "Recomendo muito",
    "Produto excelente",
    "Qualidade do atendimento ao cliente",
]

topicos_negativos = [
    "Demora no suporte ao cliente",
    "Produto com defeito",
    "Atendimento ao cliente ruim",
    "Problemas na entrega",
    "Não recomendo",
]

# Função principal que analisa as avaliações
def analise(avaliacoes, topicos_positivos=topicos_positivos, topicos_negativos=topicos_negativos):

    # Inicializa os dicionários de contagem de tópicos positivos e negativos
    contagem_positivos = {topico: 0 for topico in topicos_positivos}
    contagem_negativos = {topico: 0 for topico in topicos_negativos}

    # Analisa cada avaliação
    for i, avaliacao in enumerate(avaliacoes, start=1):
        # Cria o prompt para a análise da avaliação
        prompt = [
            {"role": "user", "content": f"Analise a avaliação: {avaliacao}. Indique se a avaliação se encaixa em algum dos tópicos positivos ({topicos_positivos}) ou negativos ({topicos_negativos}). Seja criterioso, na escolha do tópico, não classifique em qualquer um."}
        ]

        # Faz a chamada ao modelo da OpenAI para processar a avaliação
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            tools=tools,
            tool_choice="auto"
        )

        # Obtém as chamadas de ferramenta do modelo
        tool_calls = response.choices[0].message.tool_calls

        # Se houver chamadas de ferramenta, processa cada uma delas
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = funcoes_disponiveis[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # Chama a função para contabilizar os tópicos identificados
                function_to_call(topicos=function_args["topicos"], contagem_positivos=contagem_positivos, contagem_negativos=contagem_negativos)
        else:
            #print(f"Nenhum tópico identificado para a avaliação {i}: {avaliacao}")
            pass

    # Transforma as contagens em listas de dicionários
    positivos = [{"topico": tp, "contagem": count} for tp, count in contagem_positivos.items()]
    negativos = [{"topico": tn, "contagem": count} for tn, count in contagem_negativos.items()]

    return positivos, negativos

# Exemplo de uso da função de análise
# avaliacoes = [
#     "Ótimo serviço! Eles foram muito rápidos na entrega e o atendimento foi excelente.",
#     "Não recomendo. O produto veio com defeito e o suporte ao cliente foi péssimo, demoraram muito para responder.",
#     "Estou muito satisfeito com a qualidade do produto. Superou minhas expectativas!",
#     "Preço justo e entrega dentro do prazo. Recomendo!",
#     "O atendimento ao cliente foi muito ruim. Tive problemas para resolver um simples problema.",
#     "Produto excelente, superou minhas expectativas. Recomendo muito!",
#     "A entrega foi muito rápida e o produto chegou bem embalado. Serviço de qualidade.",
#     "Não gostei do produto, a qualidade deixou a desejar. Não recomendo.",
#     "Serviço muito eficiente. Eles resolveram meu problema rapidamente.",
#     "Péssimo atendimento. Fiquei esperando horas para ser atendido e ainda assim não resolveram meu problema.",
#     "Produto veio com defeito e até agora não obtive uma solução adequada."
# ]

# Chama a função de análise e armazena os resultados
# contagem_positivos, contagem_negativos = analise(avaliacoes)

# # Exibir os tópicos positivos e suas contagens
# print("Tópicos Positivos:")
# for item in contagem_positivos:
#     print(f"{item['topico']}: {item['contagem']}")
# print(contagem_positivos)

# # Exibir os tópicos negativos e suas contagens
# print("\nTópicos Negativos:")
# for item in contagem_negativos:
#     print(f"{item['topico']}: {item['contagem']}")
# print(contagem_negativos)
"""MÓDULO DE CONEXÃO COM A OPENAI"""

from openai import OpenAI
import json

# Inicializa o cliente da OpenAI com a sua chave API
client = OpenAI(api_key='meta a chave ai')

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
    "Agilidade no Serviço",
    "Variedade de Opções",
    "Sabor Agradável",
    "Ingredientes de Qualidade",
    "Pratos Apresentáveis",
    "Atendimento Bom",
    "Ambiente Confortável",
    "Bom Custo-Benefício",
    "Recomendo",
    "Voltaria",
    "Outros Positivos"
]

topicos_negativos = [
    "Lentidão no Serviço",
    "Cardápio Limitado",
    "Sabor Insatisfatório",
    "Ingredientes de Baixa Qualidade",
    "Má Apresentação dos Pratos",
    "Atendimento Ruim",
    "Ambiente Desconfortável",
    "Preços Elevados",
    "Não Recomendo",
    "Não Voltaria",
    "Outros Negativos"
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
            {"role": "user", "content": f"Analise a avaliação: {avaliacao}. Indique se a avaliação se encaixa em algum dos tópicos positivos ({topicos_positivos}) ou negativos ({topicos_negativos}). Seja criterioso, na escolha dos tópicos."}
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

    # Transforma as contagens em listas de tuplas
    positivos = dict( [(tp, count) for tp, count in contagem_positivos.items()] )
    negativos = dict( [(tn, count) for tn, count in contagem_negativos.items() ])

    return positivos, negativos


def obter_bairros(matriz): # Recebe a matriz geral

    for restaurante in matriz: # Para cada restaurante da matriz
        endereco = restaurante[5] # Pega o endereço do restaurante
        prompt = [{"role":"user", "content":f"Quero saber o é o bairro deste endereço: {endereco}. Retorne apenas o nome do bairro, com por exemplo: Centro"}]

        # Obtém o bairro do respectivo endereço

        response = client.chat.completions.create(
            messages = prompt,
            model = "gpt-3.5-turbo-0125",
            max_tokens = 50,
            temperature = 1
        )
        # Troca o antigo endereço pelo bairro
        restaurante[5] = response.choices[0].message.content



    return matriz


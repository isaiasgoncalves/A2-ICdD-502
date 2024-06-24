"""MÓDULO DE MANIPULAÇÃO DO DATASET E CRIAÇÃO DO CSV"""

import pandas as pd
import gpt



def criar_csv(matriz):

    headers = [
    "Nome",
    "Média de Estrelas",
    "Quantidade de Reviews",
    "Faixa de Preço",
    "Categoria",
    "Endereço",
    "Possui Reserva",
    "Oferece Retirada",
    "Oferece Serviço de Bufê",
    "Oferece Delivery",
    "Possui Muitas Opções Vegetarianas",
    "Possui Opções Veganas",
    "Agilidade no Serviço",
    "Lentidão no Serviço",
    "Variedade de Opções",
    "Cardápio Limitado",
    "Sabor Agradável",
    "Sabor Insatisfatório",
    "Ingredientes de Qualidade",
    "Ingredientes de Baixa Qualidade",
    "Pratos Apresentáveis",
    "Má Apresentação dos Pratos",
    "Atendimento Bom",
    "Atendimento Ruim",
    "Ambiente Confortável",
    "Ambiente Desconfortável",
    "Bom Custo-Benefício",
    "Preços Elevados",
    "Recomendo",
    "Não Recomendo",
    "Voltaria",
    "Não Voltaria",
    "Outros Positivos",
    "Outros Negativos"
    ]

    # print(len(headers))
    # Criando a base de dados
    dataset = pd.DataFrame(columns=headers)

    linha = []

    for restaurante in matriz:
        linha = restaurante[:-1]

        contagem_positivos, contagem_negativos = gpt.analise(restaurante[-1])
        for topico in contagem_positivos:
            linha.append(contagem_positivos[topico])

        for topico in contagem_negativos:
            linha.append(contagem_negativos[topico])    

        # print(linha)
        # print(len(linha))
        dataset.loc[len(dataset)] = linha

    # Resetando o índice do DataFrame e nomeando a coluna de IDs automáticos como 'IdRestaurante'
    dataset.reset_index(drop=True, inplace=True)
    dataset.index.name = 'IdRestaurante'
    


    dataset.to_csv("avaliações.csv")


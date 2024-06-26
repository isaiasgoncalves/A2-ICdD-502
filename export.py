"""MÓDULO DE MANIPULAÇÃO DO DATASET E CRIAÇÃO DO CSV"""

import pandas as pd
import gpt
import progress_bar as terminal


def criar_csv(matriz):

    # Nomes das colunas
    headers = [
    "Nome",
    "Média de Estrelas",
    "Quantidade de Reviews",
    "Faixa de Preço",
    "Categoria",
    "Bairro",
    "Possui Reserva",
    "Oferece Retirada",
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

    q = len(matriz)
    p = 1
    msg = f"Processando as informações dos restaurantes, {p} de {q}"

    for restaurante in matriz:
        
        # Printa a barra de progresso
        msg = f"Processando as informações dos restaurantes, {p} de {q}"
        terminal.prog_bar(p,q,msg)

        linha = restaurante[:-1]

        # Chama a funcão de análise de reviews do chat gpt e coloca os dados na matriz
        contagem_positivos, contagem_negativos = gpt.analise(restaurante[-1])
        for topico in contagem_positivos:
            linha.append(contagem_positivos[topico])

        for topico in contagem_negativos:
            linha.append(contagem_negativos[topico])  
        p += 1  

        # print(linha)
        # print(len(linha))
        dataset.loc[len(dataset)] = linha

    # Resetando o índice do DataFrame e nomeando a coluna de IDs automáticos como 'IdRestaurante'
    dataset.reset_index(drop=True, inplace=True)
    dataset.index.name = 'IdRestaurante'
    

    # Cria o arquivo csv e mostra uma mensagem de confirmação 
    dataset.to_csv("restaurantes.csv")
    terminal.limpar_tela()
    print("Arquivo restaurantes.csv criado!")


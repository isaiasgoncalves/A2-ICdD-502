import pandas as pd
import gpt



def criar_csv(matriz):

    headers = [
    "ID Restaurante",
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
    "Ótimo Serviço",
    "Entrega Rápida",
    "Atendimento Excelente",
    "Qualidade do Produto",
    "Recomendo",
    "Embalagem de Qualidade",
    "Eficiência no Serviço de Entrega",
    "Serviço de Qualidade",
    "Velocidade no Serviço",
    "Superou Expectativas",
    "Recomendo Muito",
    "Produto Excelente",
    "Qualidade do Atendimento ao Cliente",
    "Demora no Suporte ao Cliente",
    "Produto com Defeito",
    "Atendimento ao Cliente Ruim",
    "Problemas na Entrega",
    "Não Recomendo",
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


    


    dataset.to_csv("avaliações.csv")


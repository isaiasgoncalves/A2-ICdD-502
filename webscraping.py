"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw
import gpt

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ&sortby=review_count'
limite_paginas = 1
limite_restaurantes = 3
limite_paginas_reviews = 1  

#GERA O SOUP DO SITE GERAL
soup = [fw.gerar_soup(url)]

#GERA A LISTA DE LINKS DE RESULTADOS DA PAGINA COM TODOS OS RESTAURANTES
links_pagina = fw.gerar_listas_links(soup , "span" , "y-css-t1npoe" , limite_paginas - 1)
links_pagina.insert(0 , url)
links_pagina = fw.lista_unica(links_pagina)

#GERA A LISTA DE LINKS DE CADA RESTAURANTE
lista_soups_pagina = fw.gerar_lista_soups(links_pagina , limite_restaurantes)
links_restaurantes = fw.gerar_listas_links(lista_soups_pagina, "h3" , "y-css-hcgwj4" , limite_restaurantes)

#ORGANIZA OS LINKS PARA O FORMATO CORRETO
for i in range(len(links_restaurantes)):
    links_restaurantes[i] = "https://www.yelp.com" + links_restaurantes[i]

#GERA SOUPS DE CADA PÁGINA DE CADA RESTAURANTE
lista_soups_restaurantes = fw.gerar_lista_soups(links_restaurantes, limite_restaurantes)

#CRIA UMA LISTA COM A QUANTIDADE DE PÁGINAS DE REVIEW DE CADA RESTAURANTE
num_paginas_reviews_por_restaurante = fw.encontrar_numero_paginas_por_restaurante(lista_soups_restaurantes)

#CRIA UMA LISTA COM LISTAS DE LINKS PARA CADA PAGINA DE REVIEW
links_paginas_reviews_por_restaurante = fw.gerar_lista_links_reviews(links_restaurantes, num_paginas_reviews_por_restaurante, limite_paginas_reviews)
#Dados para coletar:
#NOME
#ESTRELAS
#QUANTIDADE DE REVIEWS
#PREÇO
#CATEGORIA
#ENDEREÇO
#AVALIAÇÕES
#TAGS DO SITE(RESERVA, TAKEOUT, CATERING, DELIVERY, OPÇÕES VEGETARIANAS)

#GERA A MATRIZ COM TODOS OS DADOS DE TODOS OS RESTAURANTES E IMPRIME ELA
restaurantes = fw.cria_matriz_dados(links_paginas_reviews_por_restaurante)
print(restaurantes)

# contagem_positivos, contagem_negativos = gpt.analise(restaurantes[0][0])
# print(contagem_positivos)
# print(contagem_negativos)

# # Exibir os tópicos positivos e suas contagens
# print("\nTópicos Positivos:") 
# for item in contagem_positivos:
#     print(f"{item['topico']}: {item['contagem']}")

# # Exibir os tópicos negativos e suas contagens
# print("\nTópicos Negativos:")
# for item in contagem_negativos:
#     print(f"{item['topico']}: {item['contagem']}")

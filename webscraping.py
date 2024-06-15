"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ&sortby=review_count'
limite_paginas = 2
limite_restaurantes = 10
limite_paginas_reviews = 10

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
restaurantes = []
lista_soups_restaurantes = fw.gerar_lista_soups(links_restaurantes, limite_restaurantes)

#CRIA UMA LISTA COM A QUANTIDADE DE PÁGINAS DE REVIEW DE CADA RESTAURANTE
lista_numero_paginas = fw.encontrar_numero_paginas_por_restaurante(lista_soups_restaurantes)

#CRIA UMA LISTA COM LISTAS DE LINKS PARA CADA PAGINA DE REVIEW
lista_de_listas_de_links_de_reviews = fw.gerar_lista_links_reviews(links_restaurantes, lista_numero_paginas, limite_paginas_reviews)

#Dados para coletar:
#NOME
#ESTRELAS
#QUANTIDADE DE REVIEWS
#PREÇO
#CATEGORIA
#ENDEREÇO
#AVALIAÇÕES
#ESTRELAS POR AVALIAÇÃO
#HORÁRIO E DATA DE FUNCIONAMENTO
#TAGS DO SITE



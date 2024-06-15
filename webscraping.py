"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ&sortby=review_count'
limite_paginas = 2
limite_produtos = 10
limite_paginas_reviews = 2

#GERA O SOUP DO SITE GERAL
soup = [fw.gerar_soup(url)]

#GERA A LISTA DE LINKS DE RESULTADOS DA PAGINA COM TODOS OS RESTAURANTES
links_pagina = fw.gerar_listas_links(soup , "span" , "y-css-t1npoe" , limite_paginas - 1)
links_pagina.insert(0 , url)
links_pagina = fw.lista_unica(links_pagina)

#GERA A LISTA DE LINKS DE CADA RESTAURANTE
lista_soups_pagina = fw.gerar_lista_soups(links_pagina , limite_produtos)
links_produtos = fw.gerar_listas_links(lista_soups_pagina, "h3" , "y-css-hcgwj4" , limite_produtos)

#ORGANIZA OS LINKS PARA O FORMATO CORRETO
for i in range(len(links_produtos)):
    links_produtos[i] = "https://www.yelp.com" + links_produtos[i]

#GERA SOUPS DE CADA PÁGINA DE CADA PRODUTO
produtos = []
lista_soups_produtos = fw.gerar_lista_soups(links_produtos, limite_produtos)

#CRIA UMA LISTA COM A QUANTIDADE DE PÁGINAS DE REVIEW DE CADA PRODUTO
lista_numero_paginas = fw.encontrar_numero_paginas_por_produto(lista_soups_produtos)



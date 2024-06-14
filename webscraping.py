"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ'

#GERA O SOUP DO SITE GERAL
soup = fw.gerar_soup(url)

#GERA A LISTA DE LINKS DE RESULTADOS DA PAGINA COM TODOS OS RESTAURANTES
links_pagina = fw.gerar_listas_paginas(soup)
links_pagina.remove(links_pagina[-1])

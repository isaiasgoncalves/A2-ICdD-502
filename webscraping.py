"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ'
limite_paginas = 10
limite_produtos = 50

#GERA O SOUP DO SITE GERAL
soup = [fw.gerar_soup(url)]

#GERA A LISTA DE LINKS DE RESULTADOS DA PAGINA COM TODOS OS RESTAURANTES
links_pagina = fw.gerar_listas_paginas(soup , "span" , "y-css-t1npoe" , limite_paginas)
links_pagina.remove(links_pagina[-1])
print(links_pagina)

lista_soups_produtos = fw.gerar_lista_soups(links_pagina , limite_produtos)
links_produtos = fw.gerar_listas_paginas(lista_soups_produtos, "h3" , "y-css-hcgwj4" , limite_produtos)
print(links_produtos)
print(len(links_produtos))
"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw
import export
import gpt

def main(limite_paginas, limite_restaurantes, limite_paginas_reviews, url):
    # Gera soup do site geral
    soup = [fw.gerar_soup(url)]
    print("Coletando links (Isso pode demorar um pouco) . . .")

    # Gera uma lista com links de páginas com todos os restaurantes
    links_pagina = fw.gerar_listas_links(soup , "span" , "y-css-t1npoe" , limite_paginas - 1)
    links_pagina.insert(0 , url)
    links_pagina = fw.lista_unica(links_pagina)

    # Gera a lista de links de todos os restaurantes
    lista_soups_pagina = fw.gerar_lista_soups(links_pagina , limite_restaurantes)
    links_restaurantes = fw.gerar_listas_links(lista_soups_pagina, "h3" , "y-css-hcgwj4" , limite_restaurantes)

    # Organiza os links no formato correto
    for i in range(len(links_restaurantes)):
        links_restaurantes[i] = "https://www.yelp.com" + links_restaurantes[i]

    # Gera soups de cada página de cada restaurante
    lista_soups_restaurantes = fw.gerar_lista_soups(links_restaurantes, limite_restaurantes)

    # Cria uma lista com a quantidade de páginas de reviews de cada restaurante
    num_paginas_reviews_por_restaurante = fw.encontrar_numero_paginas_por_restaurante(lista_soups_restaurantes)

    # Cria uma lista de lista de links de cada página de review de cada restaurante
    links_paginas_reviews_por_restaurante = fw.gerar_lista_links_reviews(links_restaurantes, num_paginas_reviews_por_restaurante, limite_paginas_reviews)

    # Gera uma matriz com todos os dados de todos os restuarantes
    restaurantes = fw.cria_matriz_dados(links_paginas_reviews_por_restaurante)

    # Transforma o endereço de cada restaurante em bairro
    restaurantes = gpt.obter_bairros(restaurantes)

    # Cria o csv com os dados da matriz
    export.criar_csv(restaurantes)
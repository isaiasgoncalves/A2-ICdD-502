"""MÓDULO PARA O WEBSCRAPING DO SITE YELP"""

import funcoes_webscraping as fw
import export
import gpt



def main(limite_paginas, limite_restaurantes, limite_paginas_reviews, url):
    #GERA O SOUP DO SITE GERAL
    soup = [fw.gerar_soup(url)]
    print("Coletando links (Isso pode demorar um pouco) . . .")

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

    #GERA A MATRIZ COM TODOS OS DADOS DE TODOS OS RESTAURANTES E IMPRIME ELA
    restaurantes = fw.cria_matriz_dados(links_paginas_reviews_por_restaurante)

    #TRANSFORMA O ENDEREÇO DE CADA RESTAURANTE EM BAIRRO
    restaurantes = gpt.obter_bairros(restaurantes)

    #CRIA O CSV COM OS DADOS DA MATRIZ
    export.criar_csv(restaurantes)
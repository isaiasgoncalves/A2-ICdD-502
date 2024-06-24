"""FUNÇÕES PARA O WEBSCRAPING"""

from bs4 import BeautifulSoup
import requests
import re

#GERA UM SOUP DADO UM URL
def gerar_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup

#GERA UMA LISTA DE LINKS DE PAGINA
def gerar_listas_links(lista_soups , tag , classe, limitador):
    links_pagina = []
    for soup in lista_soups:
        paginas = soup.find_all(tag , class_=classe)
        
        #PEGA OS BLOCOS DE CODIGOS E COLOCA EM UMA LISTA
        lista_paginas = []
        for pagina in paginas:
            if pagina.find("a"):
                lista_paginas.append(pagina.find("a"))
        
        #PROCURA APENAS OS LINKS E COLOCA NA LISTA
        for pagina in lista_paginas:
            if pagina.get("href"):
                link = pagina.get("href")
                if len(links_pagina) < limitador:
                    links_pagina.append(link)
        
    return links_pagina

#GERA UMA LISTA DE SOUPS COM UMA LISTA DE LINKS
def gerar_lista_soups(lista_links , limitador):
    lista_soups = []
    for link in lista_links:
        if len(lista_soups) < limitador:
            soup = gerar_soup(link)
            lista_soups.append(soup)
    return lista_soups

#GERA UMA LISTA DO NUMERO DE PAGINAS DE CADA RESTAURANTE    
def encontrar_numero_paginas_por_restaurante(lista_soups):
    lista_numero_paginas = []
    for soup in lista_soups:
        bloco_codigo = soup.find("div" , class_="y-css-xdax52")
        if bloco_codigo:
            string_com_numero = bloco_codigo.find("span" , class_="y-css-wfbtsu").text
            numero = string_com_numero[5:]
            numero = int(numero)
            lista_numero_paginas.append(numero)
        else:
            lista_numero_paginas.append(1)

    return lista_numero_paginas

#PEDE UMA LISTA E RETORNA UMA LISTA NA QUAL OS ELEMENTOS APARECEM UMA ÚNICA VEZ
def lista_unica(lista):
    lista_unica = []
    for elemento in lista:
        if elemento not in lista_unica:
            lista_unica.append(elemento)
    return lista_unica

#DADO A LISTA DE LINKS E QUANTIDADE DE PAGINAS POR LINK, GERA UMA LISTA DE LISTAS DE LINKS DE PAGINAS DE REVIEW
def gerar_lista_links_reviews(lista_links, lista_numeros_pagina, limitador):
    lista_links_reviews = []
    for i in range(len(lista_links)):
        links_reviews = []
        for j in range(lista_numeros_pagina[i] - 1):
            if len(links_reviews) < limitador:
                links_reviews.append(lista_links[i] + "&start=" + str(j) + "0")
        lista_links_reviews.append(links_reviews)
    
    return lista_links_reviews

#PROCURA UM DADO ESPECÍFICO EM FORMATO DE TEXTO DENTRO DE UM SOUP
def encontrar_dado(soup , tag , classe , posição):
    try:
        dado = soup.find_all(tag, class_=classe)[posição].text
    except IndexError:
        dado = ""
    return dado

#PROCURA UMA LISTA DE DADOS DENTRO DE UM SOUP
def encontrar_lista_dados(soup , tag, classe):
    if soup.find_all(tag , class_=classe):
        return soup.find_all(tag , class_=classe)

#COLETA TODAS AS AVALIAÇÕES DE UM RESTAURANTE E RETORNA UMA LISTA DELAS
def encontrar_avaliacoes(lista_links):
    avaliacoes = []
    for link in lista_links:
        soup_link = gerar_soup(link)
        bloco_codigo_avaliacoes = encontrar_lista_dados(soup_link , "p" , "comment__09f24__D0cxf y-css-h9c2fl")
        if bloco_codigo_avaliacoes:
            for bloco in bloco_codigo_avaliacoes:
                review = bloco.find("span" , class_="raw__09f24__T4Ezm")
                if review.text:
                    avaliacoes.append(review.text)
    return avaliacoes

#COLETA TAGS DE CADA RESTAURANTE, FILTRA PARA AS TAGS DESEJADAS PARA ANÁLISE E RETORNA UMA LISTA DE BOLEANOS QUE INDICAM O QUE TEM E O QUE NÃO TEM EM UM RESTAURANTE
def coletar_tags_restaurantes(soup):
    tags_true = ["Takes Reservations", "Offers Takeout" , "Offers Catering" , "Offers Delivery", "Many Vegetarian Options" , "Vegan Options"]
    tags_false = ["No Reservations", "No Takeout" , "" , "No Delivery" , "" , ""]
    lista_tag_nao_filtrada = []
    bloco_codigo_tags = encontrar_lista_dados(soup , "div" , "arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG y-css-1iy1dwt")
    if bloco_codigo_tags:
        for bloco in bloco_codigo_tags:
            tag_true = bloco.find("span" , class_="y-css-1o34y7f")
            if tag_true != None:
                lista_tag_nao_filtrada.append(tag_true.text)
            else:
                lista_tag_nao_filtrada.append("")
            tag_false = bloco.find("span" , class_="y-css-dg8xxd")
            if tag_false != None:
                lista_tag_nao_filtrada.append(tag_false.text)
            else:
                lista_tag_nao_filtrada.append("")
    lista_tag_filtrada = []
    for i in range(len(tags_true)):
        if tags_true[i] in lista_tag_nao_filtrada:
            lista_tag_filtrada.append(True)
        elif tags_false[i] in lista_tag_nao_filtrada:
            lista_tag_filtrada.append(False)
        else:
            lista_tag_filtrada.append("")
    return lista_tag_filtrada


#CRIA UMA MATRIZ COM TODOS OS RESTAURANTES E EM CADA RESTAURANTE UMA LISTA DE INFORMAÇÕES, INCLUINDO AS AVALIAÇÕES
def cria_matriz_dados(lista_lista_de_links):
    matriz = []
    for lista_links in lista_lista_de_links:
        restaurante = []
        if lista_links:
            soup = gerar_soup(lista_links[0])
            nome = encontrar_dado(soup , "h1" , "y-css-olzveb", 0)
            estrelas = encontrar_dado(soup , "span" , "y-css-kw85nd" , 0)
            if estrelas:
                estrelas = float(estrelas)
            quant_reviews = encontrar_dado(soup , "a" , "y-css-12ly5yx", 0)
            quant_reviews = re.sub("[^0-9]" , "" , quant_reviews)
            if quant_reviews:
                quant_reviews = int(quant_reviews)
            preço = encontrar_dado(soup , "span" , "y-css-33yfe" , -1)
            if preço:
                preço = len(preço)
            else:
                preço = ""
            categoria = encontrar_dado(soup , "span" , "y-css-kw85nd" , 1)
            categoria = categoria.replace("," , "")
            categoria.strip()
            endereço = encontrar_dado(soup , "p" , "y-css-dg8xxd", 0)
            restaurante.append(nome)
            restaurante.append(estrelas)
            restaurante.append(quant_reviews)
            restaurante.append(preço)
            restaurante.append(categoria)
            restaurante.append(endereço)
            lista_tags = coletar_tags_restaurantes(soup)
            restaurante = restaurante + lista_tags
            avaliacoes = encontrar_avaliacoes(lista_links)
            restaurante.append(avaliacoes)
                        
            matriz.append(restaurante)

    return matriz



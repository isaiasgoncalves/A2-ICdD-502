"""FUNÇÕES PARA O WEBSCRAPING"""

from bs4 import BeautifulSoup
import requests

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
"""FUNÇÕES PARA O WEBSCRAPING"""
from bs4 import BeautifulSoup
import requests

#GERA UM SOUP DADO UM URL
def gerar_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup

#GERA UMA LISTA DE LINKS DE PAGINA
def gerar_listas_paginas(lista_soups , tag , classe, limitador):
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
    

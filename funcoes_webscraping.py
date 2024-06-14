"""FUNÇÕES PARA O WEBSCRAPING"""
from bs4 import BeautifulSoup
import requests

#GERA UM SOUP DADO UM URL
def gerar_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup

#GERA UMA LISTA DE LINKS DE PAGINAS DE RESULTADOS
def gerar_listas_paginas(soup):
    paginas = soup.find_all("span" , class_="y-css-t1npoe")
    
    #PEGA OS BLOCOS DE CODIGOS E COLOCA EM UMA LISTA
    lista_paginas = []
    for pagina in paginas:
        if pagina.find("a"):
            lista_paginas.append(pagina.find("a"))
    
    #PROCURA APENAS OS LINKS E COLOCA NA LISTA
    links_pagina = []
    for pagina in lista_paginas:
        if pagina.get("href"):
            link = pagina.get("href")
            links_pagina.append(link)
    
    return links_pagina

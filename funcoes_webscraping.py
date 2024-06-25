"""FUNÇÕES PARA O WEBSCRAPING"""

from bs4 import BeautifulSoup
import requests
import re
import progress_bar

# Função que gera um soup dado um url
def gerar_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup

# Gera uma lista com todos os links de uma página
def gerar_listas_links(lista_soups , tag , classe, limitador):
    links_pagina = []
    for soup in lista_soups:
        paginas = soup.find_all(tag , class_=classe)
        
        # Pega todos os blocos de código e coloca em uma lista
        lista_paginas = []
        for pagina in paginas:
            if pagina.find("a"):
                lista_paginas.append(pagina.find("a"))
        
        # Procura apenas os links em cada bloco de código e coloca em uma lista
        for pagina in lista_paginas:
            if pagina.get("href"):
                link = pagina.get("href")
                if len(links_pagina) < limitador:
                    if link:
                        links_pagina.append(link)
        
    return links_pagina

# Gera uma lista de soups dado uma lista de links
def gerar_lista_soups(lista_links , limitador):
    lista_soups = []
    for link in lista_links:
        if len(lista_soups) < limitador:
            if link:   
                soup = gerar_soup(link)
                lista_soups.append(soup)
    return lista_soups

# Gera uma lista com o número de páginas de reviews de cada restaurante
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

# Dado uma lista, a função retorna outra lista sem elementos repetidos
def lista_unica(lista):
    lista_unica = []
    for elemento in lista:
        if elemento not in lista_unica:
            lista_unica.append(elemento)
    return lista_unica

# Dado uma lista de links e uma lista com o número de páginas de reviews, retorna uma lista com listas de links de paginas de reviews de cada restaurante
def gerar_lista_links_reviews(lista_links, lista_numeros_pagina, limitador):
    lista_links_reviews = []
    for i in range(len(lista_links)):
        links_reviews = []
        for j in range(lista_numeros_pagina[i] - 1):
            if len(links_reviews) < limitador:
                links_reviews.append(lista_links[i] + "&start=" + str(j) + "0")
        if links_reviews:
            lista_links_reviews.append(links_reviews)
    
    return lista_links_reviews

# Procura um dado específico dentro de um soup e retorna o texto desse dado
def encontrar_dado(soup , tag , classe , posição):
    try:
        dado = soup.find_all(tag, class_=classe)[posição].text
    except IndexError:
        dado = ""
    return dado

# Procura uma lista de dados dentro de um soup
def encontrar_lista_dados(soup , tag, classe):
    if soup.find_all(tag , class_=classe):
        return soup.find_all(tag , class_=classe)

# Coleta todas as avaliações de um restaurante e retorna uma lista com elas
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

# Coleta tags de um restaurante
def coletar_tags_restaurantes(soup):
    tags_true = ["Takes Reservations", "Offers Takeout" , "Offers Delivery", "Many Vegetarian Options" , "Vegan Options"]
    tags_false = ["No Reservations", "No Takeout" , "No Delivery" , "" , ""]
    
    # Coleta todas as tags de um restaurante
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
    
    # Seleciona apenas as tags desejadas e retorna um boleano que indica se o restaurante tem ou não uma característica
    lista_tag_filtrada = []
    for i in range(len(tags_true)):
        if tags_true[i] in lista_tag_nao_filtrada:
            lista_tag_filtrada.append(True)
        elif tags_false[i] in lista_tag_nao_filtrada:
            lista_tag_filtrada.append(False)
        else:
            lista_tag_filtrada.append(False)
    return lista_tag_filtrada


# Função que cria uma matriz com os dados de todos os restaurantes
def cria_matriz_dados(lista_lista_de_links):
    matriz = []
    p = 1
    for lista_links in lista_lista_de_links:

        # Printa a barra de progresso
        q = len(lista_lista_de_links)
        msg = f"Coletando dados dos restaurantes, {p} de {q}"
        progress_bar.prog_bar(p, q, msg)

        restaurante = []
        if lista_links:
            
            # Gera o soup de cada link e coleta o nome, caso o código não consiga coletar o nome ele retira o restaurante da matriz
            soup = gerar_soup(lista_links[0])
            nome = encontrar_dado(soup , "h1" , "y-css-olzveb", 0)
            if nome: 
                
                # Coleta os dados do restaurante
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
                categoria = categoria.strip()
                endereço = encontrar_dado(soup , "p" , "y-css-dg8xxd", 0)
                
                # Coloca os dados na matriz
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
            p += 1

    return matriz



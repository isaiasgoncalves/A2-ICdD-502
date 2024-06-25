# Trabalho da A2 de Introdução à Ciência de Dados
Projeto Final: Análise de Avaliações de Consumidores, Introdução à Ciência de Dados, Entrega: 25/06

# Feito pelos alunos:
- Isaías Gouvêa Gonçalves
- Henrique Gabriel Gasparelo
- José Thevez Gomes Guedes
  
 # Como utilizar
 1 - No arquivo `gpt.py` cole a sua chave da OpenAI no espaço indicado
 
    from openai import OpenAI
    import json

    # Inicializa o cliente da OpenAI com a sua chave API
    client = OpenAI(api_key='COLOQUE A CHAVE AQUI!!')

  2 - Abra o arquivo `main.py` e edite as informações da quantidade de restaurantes, reviews e páginas desejadas
  3 - Execute o arquivo `main.py`
  4 - O resultado da coleta de dados estará no arquivo `avaliaçoes.csv` que já possui uma prévia de como deve estar formatado no repositório original

# Documentação

## Processo do código:
![Flowchart](https://github.com/isaiasgoncalves/A2-ICdD-502/assets/88407242/274e500a-58d8-4a73-96f5-dc3ec8243af6)

1 - Utilizando as bibliotecas `requests` e `BeautifulSoup`, é criada uma lista com todas as páginas com restaurantes no site. A página principal é transformada em soup, e conforme escolhido no arquivo `main.py`, será criada uma lista com os links para as páginas

    (Arquivo webscraping.py)
    import funcoes_webscraping as fw
    import export
    import gpt
    
    def main(limite_paginas, limite_restaurantes, limite_paginas_reviews, url):
        # Gera soup do site geral
        soup = [fw.gerar_soup(url)]

2 - Para cada página, é criado um soup para análise, que são armazenados na lista lista_soups_pagina

     # Gera uma lista com links de páginas com todos os restaurantes
    links_pagina = fw.gerar_listas_links(soup , "span" , "y-css-t1npoe" , limite_paginas - 1)
    links_pagina.insert(0 , url)
    links_pagina = fw.lista_unica(links_pagina)

3 - Para cada página, é gerado uma lista de links que direcionam para cada um dos seus restaurantes

    # Gera a lista de links de todos os restaurantes
    lista_soups_pagina = fw.gerar_lista_soups(links_pagina , limite_restaurantes)
    links_restaurantes = fw.gerar_listas_links(lista_soups_pagina, "h3" , "y-css-hcgwj4" , limite_restaurantes)

4 - Para cada link de restaurante, é gerado um soup, para ser devidamente analisado

    lista_soups_restaurantes = fw.gerar_lista_soups(links_restaurantes, limite_restaurantes)

5 - O soup é analisado, e a quantidade de páginas de reviews é obtida, e é gerada uma lista de links com as páginas de avaliação

    # Cria uma lista com a quantidade de páginas de reviews de cada restaurante
    num_paginas_reviews_por_restaurante = fw.encontrar_numero_paginas_por_restaurante(lista_soups_restaurantes)

    # Cria uma lista de lista de links de cada página de review de cada restaurante
    links_paginas_reviews_por_restaurante = fw.gerar_lista_links_reviews(links_restaurantes, num_paginas_reviews_por_restaurante,   limite_paginas_reviews)
      

6 - Para cada página de review, é gerado um soup, para ser devidamente analisado 

7 - Utilizando funções de webscraping, é realizada a coleta de dados de cada um dos restaurantes 

    Os dados coletados de cada restaurante são:
    Nome,
    Média de Estrelas,
    Quantidade de Reviews,
    Faixa de Preço,
    Categoria,
    Endereço,
    Possui Reserva, *
    Oferece Retirada, *
    Oferece Delivery, *
    Possui Muitas Opções Vegetarianas, *
    Possui Opções Veganas, *
    Avaliações de Clientes

    * são tags do próprio site

8 - Para cada um dos restaurantes é criado uma lista com suas respectivas informações, que são armazenadas em string, int ou lista no caso das avaliações, que é uma lista de strings 

    # Gera uma matriz com todos os dados de todos os restuarantes
    restaurantes = fw.cria_matriz_dados(links_paginas_reviews_por_restaurante)

9 - Uma função utiliza a API do ChatGPT para tranformar o endereço do restaurante somente em bairro, o que será utilizado na análise de dados

    # Transforma o endereço de cada restaurante em bairro
    restaurantes = gpt.obter_bairros(restaurantes)

10 - Uma outra função que utiliza o ChatGPT receberá a lista de todas as reviews de um restaurante, e retornará um dicionário com a contagem de certos indicadores dentro dos reviews 


    topicos_positivos = [
     "Agilidade no Serviço",
        "Variedade de Opções",
        "Sabor Agradável",
        "Ingredientes de Qualidade",
        "Pratos Apresentáveis",
        "Atendimento Bom",
        "Ambiente Confortável",
        "Bom Custo-Benefício",
        "Recomendo",
        "Voltaria",
        "Outros Positivos"
    ]
    topicos_negativos = [
        "Lentidão no Serviço",
        "Cardápio Limitado",
        "Sabor Insatisfatório",
        "Ingredientes de Baixa Qualidade",
        "Má Apresentação dos Pratos",
        "Atendimento Ruim",
        "Ambiente Desconfortável",
        "Preços Elevados",
        "Não Recomendo",
        "Não Voltaria",
        "Outros Negativos"
    ]

Esse processo ocorre enquanto o código executa a função `export.criar_csv(restaurantes)` no arquivo `export.py`

    """MÓDULO DE MANIPULAÇÃO DO DATASET E CRIAÇÃO DO CSV"""

    import pandas as pd
    import gpt
    import progress_bar as terminal

    def criar_csv(matriz):

    (...)

    for restaurante in matriz:
        
        # Printa a barra de progresso
        msg = f"Processando as informações dos restaurantes, {p} de {q}"
        terminal.prog_bar(p,q,msg)

        

11 - Cada um dos tópicos listados será atribuido a um inteiro que representa a sua contagem, e esses inteiros serão adicionados à lista que representa cada restaurante. A lista de avaliações será removida da lista de dados do restaurante. (também ocorre em `export.py`)

    linha = restaurante[:-1]

        # Chama a funcão de análise de reviews do chat gpt e coloca os dados na matriz
        contagem_positivos, contagem_negativos = gpt.analise(restaurante[-1])
        for topico in contagem_positivos:
            linha.append(contagem_positivos[topico])

        for topico in contagem_negativos:
            linha.append(contagem_negativos[topico])  
        p += 1

12 - Assim, os dados serão todos transferidos via biblioteca Pandas para um arquivo CSV

    dataset.reset_index(drop=True, inplace=True)
    dataset.index.name = 'IdRestaurante'
    

    # Cria o arquivo csv e mostra uma mensagem de confirmação 
    dataset.to_csv("restaurantes.csv")
    terminal.limpar_tela()
    print("Arquivo restaurantes.csv criado!")

## A função de cada arquivo
### Main
  O arquivo `main.py` invoca a função que executa o código como um todo, recebendo os principais parâmetros do usuário
### Webscraping
  O arquivo ordena todos so principais processos de webscraping, organizando os principais projetos do código até a exportação dos dados
### Funções Webscraping
  Possui os principais métodos utilizados no código para extrair os dados do website desejado
### Gpt
  Possui duas funções principais, que são aquelas que utilizam a API do ChatGPT para processar e interpretar os dados a serem exportados. 
  
  A fnução `analise()` recebe a lista de avaliações e retorna o dicionário com a contagem da aparição de certos tópicos positivos listados.
  A função `obter_bairros()` recebe a lista dos restaurantes e troca o atributo 'endereço' (de índice 5) e troca pelo respectivo bairro
### Export
  O arquivo carrega a função `obter_csv()` que recebe a matriz com os dados de todos os restaurantes. Apesar do nome, a função possui outro importante papel no processamento de dados: Trocar a lista de avaliações (último elemento da lista de dados de um restaurante) pelos inteiros que representam os indicadores obtidos com a função `gpt.analise()`. Após isso, utilizando a biblioteca `pandas`, é criado um DataFrame que enfim é convertido em csv e exportado.
### Progress Bar
  Esse arquivo carrega as funções `limpar_tela()` e `prog_bar` que limpam a tela do terminal e criam uma barra de progresso que é utilizada durante alguns processos do código, respectivamente


    



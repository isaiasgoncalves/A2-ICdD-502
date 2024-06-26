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

## Excel
### Dados
  Os dados extraidos pelo webscraping e enviados para o csv foram usados em forma de tabela no Excel, foram criadas tabelas auxiliares para melhorar a visualização dos dados e a organização dos gráficos. 

#### Tabelas Auxiliares

  A primeira tabela indica, em cada restaurante, a quantidade de tópicos positivos, chamada de "Elogios", a quantidade de tópicos negativos, chamada de "Reclamações", e a diferença entre a quantidade de tópicos positivos e negativos, chamada de "Proporção".
  
  A segunda tabela retrata os meus dados das colunas dos tópicos das avaliações, porém, os mostra de forma a relativa a quantidade de tópicos de cada restaurante, representando, em um número de 0 a 100, qual a razão entre o valor daquele tópico naquele restaurante, pela quantidade total de tópicos do estabelecimento. Para cada tópico, de cada restaurante, é feita a seguinte operação, coleta o valor desse tópico, nesse restaurante, usando "PROCV", divide este valor pela quantidade de tópicos do restaurante e multiplica o resultado da divisão por 100.
### Escolha das análises
  A apresentação dos dados foi dividida em 3 peças de análise:

#### Bairros

  Foram escolhidos 4 gráficos para análise, a partir de tabelas dinâmicas criadas em outra aba:

  Bairro X Média de Estrelas e Quantidade de Reviews - Relaciona para cada bairro qual a média da média de estrelas e a média de quantidade de reviews, foi escolhido a fim de analisar em quais locais existem os restaurantes melhor avaliados e com mais avaliações. O gráfico é uma combinação de coluna e linha para promover comparações, entre as localidades, estrelas e reviews de diversas formas.

  Bairro X Proporção - Relaciona para cada bairro a diferença entre tópicos positivos e negativos, foi escolhido com o intuito de analisar quais locais são mais ou menos elogiados. O tipo de gráfico é gráfico de colunas para facilitar a visualização.

  Bairro X Quantidade - Relaciona para cada bairro a quantidade de restaurantes, foi escolhido a fim de entender em quais locais existem mais restaurantes. O tipo de gráfico é gráfico de colunas para facilitar a visualização.

  Bairro X Custo-Benefício - Relaciona para cada bairro o custo-benefício médio, foi escolhido para entender em quais bairros os restaurantes possui maior ou menor custo-benefício. O gráfico preferido foi de colunas empilhadas para comparar entre bairros e analisar cada um deles.

  A apresentação de todos esses gráficos foi feita com o intuito de comparar, buscar tendências e encontrar pontos de melhoria em cada bairro, entendendo em quais bairros estão os melhores restaurantes.

#### Faixa de preço

  Foram escolhidos 4 gráficos para análise, a partir de tabelas dinâmicas criadas em outra aba:

  Faixa de Preço X Média de Estrelas - Relaciona para cada faixa de preço qual a média da média de estrelas, foi escolhido com o intuito de analisar em qual faixa de preço se encontra os restaurantes melhor avaliados. O tipo de gráfico é gráfico de colunas para facilitar a visualização.

  Faixa de Preço X Quantidade - Relaciona para cada faixa de preço a quantidade de restaurantes, foi escolhido a fim de entender em qual faixa de preço se encontra a maioria dos restaurantes. O tipo de gráfico é gráfico de colunas para facilitar a visualização.

  Faixa de Preço X Retorno dos Clientes - Relaciona para cada faixa de preço a média dos valores do tópico "Voltaria", foi escolhido com a intenção de entender qual a faixa de preço que atrai os clientes o bastante para que eles retornem ao estabelecimento. O tipo de gráfico é gráfico de linhas, para entender conforme a faixa de preço aumenta o que acontece com o retorno dos clientes.

  Faixa de Preço X Recomendações do Clientes - Relaciona para cada faixa de preço a média dos valores do tópico "Recomendo", foi escolhido com a intenção de entender qual a faixa de preço que incentiva os clientes a recomendar o restaurante para conhecidos. O tipo de gráfico é gráfico de linhas, para entender conforme a faixa de preço aumenta o que acontece com as recomendações dos clientes.

  A apresentação de todos esses gráficos foi feita com o intuito de entender como a faixa de preço influencia as avaliações, o retorno, as recomendações e as opiniões dos clientes no ramo de restaurantes, buscando encontrar padrões e pontos de melhoria.

#### Categorias

  Foram escolhidos 4 gráficos para análise, a partir de tabelas dinâmicas criadas em outra aba:

  Categorias X Variedade: Relaciona para cada categoria qual a média dos valores dos tópicos relacionados a variedade de opções e limitações do cardápio, foi escolhido com a intenção de entender quais são as categorias de restaurantes que possui maior variedade de produtos. O tipo de gráfico é gráfico de colunas empilhadas, para comparar categorias e analisar cada uma delas.

  Categorias X Proporção: Relaciona para cada categoria qual a diferença entre tópicos positivos e negativos, foi escolhido para entender quais são as categorias melhor avaliadas. O tipo de gráfico é gráfico de colunas para facilitar a visualização.

  Categorias X Apresentação dos Pratos: Relaciona para cada categoria qual a média dos valores dos tópicos relacionados a apresentação dos pratos, foi escolhido para entender em quais categorias os restaurantes possuem uma melhor apresentação dos pratos. O tipo de gráfico é gráfico de colunas empilhadas, para comparar categorias e analisar cada uma delas.

  Categorias X Sabor: Relaciona para cada categoria qual a média dos valores relacionados ao sabor dos pratos, foi escolhido com o intuito de compreender quais categorias de restaurantes possuem pratos mais saborosos. O tipo de gráfico é gráfico de colunas empilhadas, para comparar categorias e analisar cada uma delas.

  A apresentação de todos esses gráficos foi feita com o intuito de comparar categorias de restaurantes, buscar padrões entre as categorias com melhor variedade, sabor, qualidade e apresentação dos pratos, e entender pontos onde cada categoria pode melhorar.

### Conclusões

  A partir dos dados coletados e dos gráficos apresentados é possível concluir o seguinte sobre cada uma das peças de análise:

#### Bairros

  Bairros como a Lapa, possuem muitas avaliações e uma grande satisfação dos clientes, o que evidencia que um aumento no número de avaliações pode ajudá-lo a melhorar seus serviços.
  Bairros da zona Sul, como Copacabana, Ipanema e Leblon, possuem mais restaurantes, mostrando que certas áreas precisam de mais restaurantes.
  Bairros como a Lapa, Botafogo e Santa Teresa possuem preços mais elevados, enquanto Del Castilho e Copacabana possuem maior custo-benefício, mostrando quais restaurantes precisam melhores os preços.
  Existem filtros no Excel por faixa de preço, oferta de delivery e oferta de retirada, o que possibilita análises mais específicas.

#### Faixa de Preço

  Restaurantes mais baratos, na faixa de preço 2, possuem maior quantidade de estrelas, o que mostra que restaurante mais baratos são melhor avaliados e que o alto preço de certos restaurantes pode ser um problema para a qualidade do serviço.
  Quanto mais caro for o restaurante, maior a quantidade de pessoas que voltaria neles, o que mostra que a experiência de restaurantes mais caros é boa o bastante para motivar os clientes a irem novamente.
  Quanto mais caro for o restaurante, maior a quantidade de pessoas que recomendaria eles, mostrando que restaurantes mais caros oferecem uma experiência que motiva os clientes a recomendá-los para conhecidos.
  A maior quantidade de restaurantes são da categoria 3, o que mostra que os preços dos restaurantes são equilibrados.
  Existem filtros no Excel por bairro, oferta de opções vegetarianas e oferta de opções veganas, o que possibilita análises mais específicas.

#### Categoria

  A maioria das categorias possuem uma grande variedade de opções no menu, dentre elas, Gastropub e Breweries são as que possuem a maior variedade.
  A categoria Bistro é a que mais possui satisfação dos clientes, o que evidencia que serviços como esse são mais satisfatórios aos clientes, enquanto Salad possui baixa satisfação com os clientes, mostrando que serviços como esse são menos atratativos.
  A maioria das categorias são equilibradas quanto a boa e má apresentação dos pratos, o que mostra que esse aspecto, embora não esteja ruim, precisa de melhorias para potencializar a qualidade do serviço.
  Boa parte das categorias são equilibradas quanto ao sabor ser satisfatório ou desagradável, o que mostra que esse aspecto, também precisa de melhorias, mas certas categorias, como Breweries possui sabor totalmente insatisfatório, mostrando que o sabor é algo que precisa ser completamente melhorado em certas categorias, pois pode representar sérios problemas aos restaurantes delas.
  Existem filtros no Excel por bairro, faixa de preço e oferta de reserva, o que possibilita análises mais específicas.
    



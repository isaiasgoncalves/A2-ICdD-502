"""ARQUIVO PRINCIPAL"""

import webscraping as ws

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ&sortby=review_count'

pag = 2 # Limite de páginas
rest = 10 # Limite de restaurantes
rev = 3  # Limite de páginas de reviews

ws.main(pag, rest, rev, url)
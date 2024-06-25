import webscraping as ws

url = 'https://www.yelp.com/search?find_desc=restaurants&find_loc=Rio+de+Janeiro%2C+RJ&sortby=review_count'

pag = 1 # Limite de páginas
rest = 3 # Limite de restaurantes
rev = 1  # Limite de reviews

ws.main(pag, rest, rev, url)
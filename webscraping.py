''' módulo de webscraping para o site do airbnb '''

from bs4 import BeautifulSoup
import requests

url = 'https://www.airbnb.com.br/rooms/785597352085876502/reviews?search_mode=regular_search&check_in=2024-06-28&check_out=2024-07-05&source_impression_id=p3_1718279778_P30DN7DV9Zlm_Sra&previous_page_section_name=1000&federated_search_id=9b720ddc-8faa-490f-bd01-edcbf97ca079'
page = requests.get(url)



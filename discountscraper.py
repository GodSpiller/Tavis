import requests, json, spacy, database
from discount import Discount, Catalogue
import psycopg2
from sshtunnel import SSHTunnelForwarder
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response
from utility import compute_similarity_discount

def scraper(catalogue):
    try:
        link = 'https://etilbudsavis.dk/api/squid/v2/catalogs/{catId}/hotspots'.format(
            catId = catalogue.catalogue_id
        )
        
        response = json.loads(requests.get(link).text)
        discounts = []

        for offer in response:
            discount_offer = Discount()
            discount_offer.title = offer['offer']['heading']
            discount_offer.price = offer['offer']['pricing']['price']
            discount_offer.unit = offer['offer']['quantity']['unit']['symbol']
            discount_offer.amount = str(offer['offer']['quantity']['size']['from'])
            discount_offer.amount += '-' + str(offer['offer']['quantity']['size']['to'])            
            discount_offer.valid_from = offer['offer']['run_from'].split("T")[0]
            discount_offer.valid_to = offer['offer']['run_till'].split("T")[0]
            discount_offer.catalogue_id = catalogue.catalogue_id
            
            discounts.append(discount_offer)

    except Exception as e: print(e)
    
    return discounts

def get_all_catalogs(url):
    catalogues = []

    rp=RobotFileParser()
    rp.set_url(url)
    rp.read()
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, 'html.parser')
    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)
  
    for i in data['props']['reactQueryState']['queries']:
        if ('ern' in i['state']['data']):
            if (i['state']['data']['ern'].split(":")[1] == 'catalog'):
                catalogue = Catalogue()
                catalogue.store_name = i['state']['data']['branding']['name']
                catalogue.catalogue_id = i['state']['data']['id']   
                
                catalogues.append(catalogue)

    return catalogues



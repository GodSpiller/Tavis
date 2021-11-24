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
        link = "https://etilbudsavis.dk/api/squid/v2/catalogs/{catId}/hotspots".format(
            catId = catalogue.catalogue_id
        )
        #Insert catalogue in database function call
        response = json.loads(requests.get(link).text)
        discounts = []

        for offer in response:
            discount_offer = Discount()
            #title
            discount_offer.title = offer['offer']['heading']
            #price
            discount_offer.price = offer['offer']['pricing']['price']
            #unit symbol        
            discount_offer.unit = offer['offer']['quantity']['unit']['symbol']
            #amount   
            discount_offer.amount = str(offer['offer']['quantity']['size']['from'])
            discount_offer.amount += "-" + str(offer['offer']['quantity']['size']['to']) 
            
            
            #fra og til
            discount_offer.valid_from = offer['offer']['run_from'].split("T")[0]
            discount_offer.valid_to = offer['offer']['run_till'].split("T")[0]

            discount_offer.catalogue_id = catalogue.catalogue_id
            
            discounts.append(discount_offer)

            '''if offer_amount != None:
                best_match = compute_similarity_discount(discount_offer.title, match_dict, offer_amount)

            if best_match != [] and best_match != None:
                for x in best_match:
                    print(discount_offer.title + " : " + str(x[0]))
            '''
            #Insert discount product in database function call

    except Exception as e: print(e)
    
    return discounts

def get_all_catalogs(url):
    catalogues = []

    rp=RobotFileParser()
    rp.set_url(url)
    rp.read()
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, "html.parser")
    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)
  
    for i in data['props']['reactQueryState']['queries']:
        if ('ern' in i['state']['data']):
            if (i['state']['data']['ern'].split(":")[1] == 'catalog'):
                catalogue = Catalogue()
                catalogue.store_name = i['state']['data']['branding']['name']
                catalogue.catalogue_id = i['state']['data']['id']   
                
                catalogues.append(catalogue)

    return catalogues



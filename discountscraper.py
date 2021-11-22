import requests, json, database, spacy
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
        combo_date = ""
        highest = 0
        dates_dict = {}
        response = json.loads(requests.get(link).text)
        print(catalogue.store_name)

        for offer in response:
            discount_offer = Discount()
            #title
            discount_offer.title = offer['offer']['heading']
            #price
            discount_offer.price = offer['offer']['pricing']['price']
            #unit symbol        
            discount_offer.unit = offer['offer']['quantity']['unit']['si']
            #amount   
            discount_offer.amount = offer['offer']['quantity']['size']
            #fra og til
            discount_offer.valid_from = offer['offer']['run_from'].split("T")[0]
            discount_offer.valid_to = offer['offer']['run_till'].split("T")[0]
            combo = discount_offer.valid_from + " : " + discount_offer.valid_to
            offer_amount = len(discount_offer.title.replace(" eller ", ",").split(","))
            if offer_amount != None:
                temp = compute_similarity_discount(discount_offer.title, match_dict, offer_amount)
            if temp != [] and temp != None:
               print(discount_offer.title + " : " + str(temp))

            if combo in dates_dict:
                dates_dict[combo] += 1
            else:
                dates_dict[combo] = 1
        
        for key in dates_dict.keys():
            if dates_dict[key] > highest:
                highest = dates_dict[key]
                combo_date = key

        dates = combo_date.split(':')
        catalogue.valid_from = dates[0]
        catalogue.valid_to = dates[1]
    except Exception as e: print(e)
    
def get_all_catalogs(url):
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
                
                scraper(catalogue)

rp=RobotFileParser()
urllink = "https://etilbudsavis.dk/discover/groceries"

nlp = spacy.load('da_core_news_lg')

match_dict = {}
categories = database.fetch_ingredients()

for category in categories:
    match_dict[category] = nlp(category.lower())

get_all_catalogs(urllink)

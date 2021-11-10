import requests, json, database
import psycopg2
from sshtunnel import SSHTunnelForwarder
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response


def scraper(catalogId):
    link = "https://etilbudsavis.dk/api/squid/v2/catalogs/{catId}/hotspots".format(
        catId = catalogId
    )
    response = json.loads(requests.get(link).text)

    for offer in response:
        #title
        print(offer['offer']['heading'])
        #price
        print(offer['offer']['pricing']['price'])
        #unit symbol             
        print(offer['offer']['quantity']['unit']['si'])
        #amount   
        print(offer['offer']['quantity']['size'])
        #fra og til
        print(offer['offer']['run_from'])
        print(offer['offer']['run_till'])


def getAllCatalogs(url):
    rp.set_url(url)
    rp.read()
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, "html.parser")
    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

  
    for i in data['props']['reactQueryState']['queries']:
        if ('ern' in i['state']['data']):
            if (i['state']['data']['ern'].split(":")[1] == 'catalog'):
                print('{store} ({storeId}) - Catalogue: ({catId})'.format(
                    store = i['state']['data']['branding']['name'],
                    storeId = i['state']['data']['dealerId'],
                    catId = i['state']['data']['id']
                ))
                scraper(i['state']['data']['id'])

rp=RobotFileParser()
urllink = "https://etilbudsavis.dk/discover/groceries"

conn = database.connectToDB()
cur = conn.cursor()
cur.execute("SELECT * FROM chains")

for row in cur.fetchall():
    print(row[1])

cur.close()
conn.close()

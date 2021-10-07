import requests, json
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response


def scraper(catalogId):
    link = "https://etilbudsavis.dk/api/squid/v2/catalogs/{catId}/hotspots".format(
        catId = catalogId
    )
    response = json.loads(requests.get(link).text)

    for offer in response:
        print(offer['offer']['heading'])
        print(offer['offer']['pricing']['price'])

def recipeScraper(list):
    for url in list:
        r=requests.get(url)
        r_parse = BeautifulSoup(r.content, "html.parser")

        print(url)
        for list in r_parse.find_all('li', {"class" : "components"}):
               print(list.text)
            
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

def getAllRecipes(url):
    rp.set_url(url)
    rp.read() 
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, "html.parser")

    listOfSites = []
    

    for link in r_parse.find_all('a'):
        if link.get('href') != None and "https://mummum.dk/" in link.get('href') and link.get('href') not in listOfSites:
            
            listOfSites.append(link.get('href'))
            #print(link)
            #print(link.name)

    return listOfSites

rp=RobotFileParser()

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"

#getAllCatalogs(urllink)
recipeScraper(getAllRecipes(urllink2))
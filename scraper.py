import requests, json
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response

bannedList = [
    "https://mummum.dk/shop/kogebog-mummums-hverdagsfavoritter/",
    "https://mummum.dk/category/opskrifter/drikkevarer/",
    "https://mummum.dk/madplaner/",
    "https://mummum.dk/medlemskab/",
    "https://mummum.dk/kogeboeger/",
    "https://mummum.dk/min-konto/",
    "https://mummum.dk/",    
    "https://mummum.dk/tag-selv-hotdogbar/",
    "https://mummum.dk/tips-og-tricks/",
    "https://mummum.dk/inspiration/",
    "https://mummum.dk/om-os/",
    "https://mummum.dk/abonnementsbetingelser/",
    "https://mummum.dk/handelsbetingelser/",
    "https://mummum.dk/kontakt/",
    "https://mummum.dk/pastaretter/",
    "https://mummum.dk/?page_id=6473",
    "https://mummum.dk/?p=4599",
    "https://mummum.dk/opskrifter/",
    "https://mummum.dk/opskrifter/morgenmad-og-brunch/",
    "https://mummum.dk/opskrifter/bagvaerk/",
    "https://mummum.dk/opskrifter/frokost/",
    "https://mummum.dk/opskrifter/dyppelse/",
    "https://mummum.dk/opskrifter/aftensmad/",
    "https://mummum.dk/opskrifter/salater-og-tilbehoer/",
    "https://mummum.dk/opskrifter/soede-sager/",
    "https://mummum.dk/opskrifter/sundere-alternativer/",
    "https://mummum.dk/opskrifter/tapas/",
    "https://mummum.dk/opskrifter/aftensmad/grillmad/",
    "https://mummum.dk/opskrifter/aftensmad/graesk-mad/",
    "https://mummum.dk/opskrifter/aftensmad/mexicansk-mad/",
    "https://mummum.dk/opskrifter/aftensmad/italiensk-mad/",
    "https://mummum.dk/opskrifter/aftensmad/asiatisk-mad/",
    "https://mummum.dk/opskrifter/aftensmad/burger/",
    "https://mummum.dk/opskrifter/aftensmad/dansk-mad/",
    "https://mummum.dk/opskrifter/aftensmad/frikadeller/",
    "https://mummum.dk/opskrifter/aftensmad/gryderetter/",
    "https://mummum.dk/opskrifter/aftensmad/lasagne/",
    "https://mummum.dk/opskrifter/aftensmad/one-pot-retter/",
    "https://mummum.dk/opskrifter/aftensmad/pastaretter/",
    "https://mummum.dk/opskrifter/aftensmad/pizza/",
    "https://mummum.dk/opskrifter/aftensmad/retter-i-fad/",
    "https://mummum.dk/opskrifter/aftensmad/supper/",
    "https://mummum.dk/opskrifter/aftensmad/taerter/",
    "https://mummum.dk/opskrifter/aftensmad/tilberedning-af-fisk/",
    "https://mummum.dk/opskrifter/aftensmad/tilberedning-af-fjerkrae/",
    "https://mummum.dk/opskrifter/aftensmad/tilberedning-af-oksekoed/",
    "https://mummum.dk/opskrifter/aftensmad/tilberedning-af-svinekoed/",
    "https://mummum.dk/kylling-i-svampesauce-med-rodfrugtmos/"]

def scraper(catalogId):
    link = "https://etilbudsavis.dk/api/squid/v2/catalogs/{catId}/hotspots".format(
        catId = catalogId
    )
    response = json.loads(requests.get(link).text)

    for offer in response:
        print(offer['offer']['heading'])
        print(offer['offer']['pricing']['price'])

def recipeScraper(list):
    listOfLists = []

    for url in list:
        r=requests.get(url)
        r_parse = BeautifulSoup(r.content, "html.parser")

        tempList = []
        listOfTitles = []
        listOfAmount = []
        listOfUnits = []
        listOfIngredients = []

        #print('"', url, '",')
        if not r_parse.find('h3', text="Ingrediensliste"):
            #print("skip")
            sleep(0.1)
        else:
            listOfTitles.append(r_parse.find("h1", {"class" : "entry-title hyphen"}).text)
            print(r_parse.find("h1", {"class" : "entry-title hyphen"}).text)
            for li in r_parse.find_all('li', {"class" : "components"}):
                for span in li.find_all('span'):
                    tempList.append(span.text)
                    #print(span.text)
                    #listOfIngredients.append(list.text.replace('\n', ' '))
                
            for i in range(len(tempList)):
                if (i % 3 == 0): #0 == amount
                    listOfAmount.append(tempList[i])
                if (i % 3 == 1): #1 == units
                    listOfUnits.append(tempList[i])
                if (i % 3 == 2): #2 == ingredients
                    listOfIngredients.append(tempList[i])
            print(tempList)

            listOfLists.append(listOfIngredients)
            sleep(1)

    return listOfLists              
                       
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
        href = link.get('href')
        if href != None and "https://mummum.dk/" in href and href not in listOfSites and href not in bannedList:   
            listOfSites.append(link.get('href'))
            #print(link)
            #print(link.name)

    recipeScraper(listOfSites)
    #return listOfSites

rp=RobotFileParser()

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"

#getAllCatalogs(urllink)
#hyplink = getAllRecipes(urllink2)

rec = recipeScraper(getAllRecipes(urllink2))


#recipeScraper(["https://mummum.dk/spaghetti-bolognese/", "https://mummum.dk/lakseret/"])
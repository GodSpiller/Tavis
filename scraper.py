import requests, json
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser

def skraper(storeID, catId):

    url = 'https://etilbudsavis.dk/business/{dealerid}/publications/{catalogid}/paged'.format(
        dealerid = storeID,
        catalogid = catId
    )

    rp.set_url(url)
    rp.read()

    r=requests.get(url)

    r_parse = BeautifulSoup(r.text, 'html.parser')

    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

    for i in data['props']['reactQueryState']['queries']:
        if ('ern' in i['state']['data']):
            if(i['state']['data']['ern'].split(":")[1] == "offer"):
                print("    " + i['state']['data']['heading'])

def etellerandet(url):
    rp.set_url(url)
    rp.read()
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, "html.parser")
    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

    num = 1
    for i in data['props']['reactQueryState']['queries']:
        if ('ern' in i['state']['data']):
            if (i['state']['data']['ern'].split(":")[1] == 'catalog'):
                print('{store} ({storeId}) - Catalogue: ({catId})'.format(
                    store = i['state']['data']['branding']['name'],
                    storeId = i['state']['data']['dealerId'],
                    catId = i['state']['data']['id']
                ))
                skraper(i['state']['data']['dealerId'], i['state']['data']['id'])
    
    """
    for i in range (len(data['props']['reactQueryState']['queries'])):

        if ('ern' in data['props']['reactQueryState']['queries'][i]['state']['data']):
            if (data['props']['reactQueryState']['queries'][i]['state']['data']['ern'].split(':')[1] == 'catalog'):
                skraper('https://etilbudsavis.dk/business/{dealerid}/publications/{catalogid}/paged'.format(
                    dealerid = data['props']['reactQueryState']['queries'][i]['state']['data']['dealerId'],
                    catalogid = data['props']['reactQueryState']['queries'][i]['state']['data']['id']
                ))
                print(data['props']['reactQueryState']['queries'][i]['state']['data']['branding']['name'])
    """


rp=RobotFileParser()

urllink = "https://etilbudsavis.dk/discover/groceries"

etellerandet(urllink)

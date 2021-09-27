import requests, json
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser

def skraper(url):
    rp.set_url(url)
    rp.read()

    r=requests.get(url)

    r_parse = BeautifulSoup(r.text, 'html.parser')

    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

    for i in range (len(data['props']['reactQueryState']['queries'])):
        if (data['props']['reactQueryState']['queries'][i]['state']['data']['ern'].split(':')[1] == 'offer'):
            print(data['props']['reactQueryState']['queries'][i]['state']['data']['offer']['heading'])


def etellerandet(url):
    rp.set_url(url)
    rp.read()
    
    r=requests.get(url)
    r_parse = BeautifulSoup(r.text, "html.parser")
    data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

    for i in range (len(data['props']['reactQueryState']['queries'])):
        if ('ern' in data['props']['reactQueryState']['queries'][i]['state']['data']):
            if (data['props']['reactQueryState']['queries'][i]['state']['data']['ern'].split(':')[1] == 'catalog'):
                skraper('https://etilbudsavis.dk/business/{dealerid}/publications/{catalogid}/paged'.format(
                    dealerid = data['props']['reactQueryState']['queries'][i]['state']['data']['dealerId'],
                    catalogid = data['props']['reactQueryState']['queries'][i]['state']['data']['id']
                ))
                print(data['props']['reactQueryState']['queries'][i]['state']['data']['branding']['name'])


rp=RobotFileParser()

urllink = "https://etilbudsavis.dk"

etellerandet(urllink)




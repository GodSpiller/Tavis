import requests, json
from bs4 import BeautifulSoup
from time import sleep
from urllib.robotparser import RobotFileParser

rp=RobotFileParser()

urllink = "https://etilbudsavis.dk/businesses/101cD/publications/FzKCNPup/paged"

rp.set_url(urllink)
rp.read()
print(rp.can_fetch("*", urllink))

r=requests.get(urllink)

r_parse = BeautifulSoup(r.text, 'html.parser')

data = json.loads(r_parse.find('script', type='application/json', id='__NEXT_DATA__').text)

for x in data['props']['reactQueryState']['queries'][3]['state']['data']:
    print(x['offer']['heading'])



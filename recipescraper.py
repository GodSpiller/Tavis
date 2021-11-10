import requests, json
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response
from database import connectToDB
import psycopg2

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


def recipeScraper(list):
    listOfTitles = []
    listOfTime = []
    listOfAmount = [],[]
    listOfUnits = [],[]
    listOfIngredients = [],[]
    count = 0


    for url in list:
        r=requests.get(url)
        r_parse = BeautifulSoup(r.content, "html.parser")

        tempList = []

        #print('"', url, '",')
        if not r_parse.find('h3', text="Ingrediensliste"):                                  #Looks for title with ID="Ingrediensliste"
            #print("skip")
            sleep(0.1)
        else:                                                                               #if ID="Ingrediensliste" is found
            listOfTitles.append(r_parse.find("h1", {"class" : "entry-title hyphen"}).text)
            listOfTime.append(r_parse.find())                                               #Find samlet tid------------------------------------------------------------------------
            print(r_parse.find("h1", {"class" : "entry-title hyphen"}).text)
            for li in r_parse.find_all('li', {"class" : "components"}):
                for span in li.find_all('span'):
                    tempList.append(span.text)
                    #print(span.text)
                    #listOfIngredients.append(list.text.replace('\n', ' '))
                
            for i in range(len(tempList)):
                if (i % 3 == 0): #0 == amount
                    listOfAmount[count].append(tempList[i])
                if (i % 3 == 1): #1 == units
                    listOfUnits[count].append(tempList[i])
                if (i % 3 == 2): #2 == ingredients
                    listOfIngredients[count].append(tempList[i])
            print(tempList)

            
            sleep(1)  

        count += 1

                     

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

    return listOfSites
    #return listOfSites

def uploadToDB(list):
    sql = """INSERT INTO """
    try:
        # read database configuration
        #params = config()
        # connect to the PostgreSQL database
        conn = connectToDB()
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

rp=RobotFileParser()
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"




recipeScraper(getAllRecipes(urllink2))

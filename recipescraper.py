import requests, json, utility, database, editDistance, spacy
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response


def recipeScraper(urls):
    recipes = []
    categories = database.fetch_categories()
    match_dict = {}
    recurrence_dict = {}

    for category in categories:
        match_dict[category] = nlp(category.lower().replace(",", "").replace("rå", ""))

    for url in urls or []:
        try:
            r=requests.get(url)
            r_parse = BeautifulSoup(r.content, "html.parser")

            if r_parse.find('h3', text="Ingrediensliste"):
                tempList = []
                amounts = []
                units = []
                ingredients = []
                instructions = ""
                mealType = ''
                quantity = 1 
                amountUnit = ''
                
                # Gets the title of the recipe
                title = r_parse.find("h1", {"class" : "entry-title hyphen"}).text

                # Number of people
                for select in r_parse.find_all('select', { 'class' : 'single-recipe-amount'}):
                    for option in select.find_all('option', { 'selected' : 'selected' }):
                        quantity = int(option.text)

                # Gets the time it takes to make the recipe
                time = r_parse.find("div", {"class" : "recipe-total"}).text
                time = time.split('\t')
                time = time[len(time) - 1]

                time = utility.convertToMinutes(time)

                # Finds the html with ingredients that also contains unit and amount
                for li in r_parse.find_all('li', {"class" : "components"}):
                    for span in li.find_all('span'): #print(span.text)
                        tempList.append(span.text) #listOfIngredients.append(list.text.replace('\n', ' '))

                # Preprocess ingredients into three seperate lists: item, unit and amount
                for i in range(0, len(tempList), 3):

                    # Remove. Probably? Or not.
                    if tempList[i + 2] == 'salt/peber':
                        continue

                    # Normalizes the value to one person/piece
                    if tempList[i] !=  '':
                        amounts.append(float(tempList[i].replace(',', '.')) / quantity)
                    else:
                        amounts.append(tempList[i])

                    units.append(tempList[i + 1])
                    ingredients.append(tempList[i + 2])

                # Instructions for the recipe
                for div in r_parse.find_all('div', {'class' : 'recipe-procedure'}):
                    for ol in div.find_all('ol'):
                        for li in ol.find_all('li'):
                            instructions = instructions + "|"  + li.text

                
                # Type of meal (Dinner, breakfast, etc.)
                for p in r_parse.find_all('p', { 'class' : 'breadcrumbs' }):
                    mealType = p.text

                mealType = mealType.split(' / ')
                mealType = mealType[2]

                # Unit amount
                for span in r_parse.find_all('span', { 'class' : 'recipe-amount-select'}):
                    amountUnit = span.text

                amountUnit = amountUnit.replace('\t', '').split(' ')
                amountUnit = amountUnit[len(amountUnit) - 1]

                image = str(r_parse.find("div", {'class' : 'recipe-image'})).split('"')[15].split(",")[0].split(" ")[0]

                print(title)

                for elem in ingredients:
                    match = editDistance.compute_similarity(elem, match_dict)
                    print(elem + " : " + match)
                    elem_match = elem + " : " + match
                    if elem_match in recurrence_dict:
                        recurrence_dict[elem_match] += 1
                    else:
                        recurrence_dict[elem_match] = 1
                print("---------------------------------------")
                    
                #database.insertRecipe(title, instructions, image, amountUnit, time, mealType)
                #database.insertIngredients(title, ingredients, units, amounts) 

                '''print('\n\nTitle: ' + title)
                print('Image: ' + image)
                print('Time: ' + str(time))
                print('Type: ' + mealType)
                print('Unit: ' +  amountUnit)
                print('--------Ingredients---------')
                
                for i in range(len(amounts)):
                    print(amounts[i], units[i], ingredients[i])


                print('--------Instructions---------')
                print(instructions)

                print('-----------------------------')
                '''
                sleep(1)
            else:
                sleep(0.1)
        except Exception as e: print(e)

    return recurrence_dict 

def getAllRecipes(urls, listOfSitesFound):
    wantToCrawl = []
    for url in urls:
        rp.set_url(url)
        rp.read() 
        
        r=requests.get(url)
        r_parse = BeautifulSoup(r.text, "html.parser")

        for link in r_parse.find_all('a'):                                                      #Finds all links in url
            href = link.get('href')                                                             #Extracts link from html class
            if href != None and "https://mummum.dk/" in href and href not in listOfSitesFound:  #Ensures that crawler stays on mummum.dk and not visits the same site twice
                if "?page" in href and href not in listOfSitesFound:                            #Checks if href is a link the crawler should crawl
                    wantToCrawl.append(href)                                                    #Add href to wantToCrawl list
                listOfSitesFound.append(href)                                                   #Add href to lsitOfSitesFound

    if wantToCrawl:                                                                       # If empty == false
        getAllRecipes(wantToCrawl,listOfSitesFound)
    return listOfSitesFound

rp=RobotFileParser()
nlp = spacy.load('da_core_news_lg')
#Morgen-, Middag-, Aftensmad, og tilbehør til aftensmad
urllink1 = ["https://mummum.dk/opskrifter/aftensmad/", "https://mummum.dk/opskrifter/morgenmad-og-brunch/",
            "https://mummum.dk/opskrifter/frokost/",
            "https://mummum.dk/opskrifter/salater-og-tilbehoer/"]

#Alle opskrifter
urllink2 = ["https://mummum.dk/opskrifter"] 
rec_dict = recipeScraper(getAllRecipes(urllink1, []))

file = open('rec.txt', 'w', encoding='utf-8')
for key in rec_dict:
    file.write(str(key) + " | " + str(rec_dict[key]) + "\n")

file.close()

#recipeScraper(["https://mummum.dk/graeskarfritter/", "https://mummum.dk/brunede-kartofler/i-ovn/"])

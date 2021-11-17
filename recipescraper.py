import requests, json, utility, database, editDistance, spacy
from recipe import Recipe
from bs4 import BeautifulSoup
from time import process_time_ns, sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response


def recipeScraper(urls):
    categories = database.fetch_ingredients()
    match_dict = {}
    recipes = []
    x = 1

    for category in categories:
        match_dict[category] = nlp(category.lower().replace(",", "").replace("rå", ""))

    for url in urls or []:
        try:
            r=requests.get(url)
            r_parse = BeautifulSoup(r.content, "html.parser")

            if r_parse.find('h3', text="Ingrediensliste"):
                recipe = Recipe()
                tempList = []
             
                # Gets the title of the recipe
                recipe.title = r_parse.find("h1", {"class" : "entry-title hyphen"}).text

                # Number of people
                for select in r_parse.find_all('select', { 'class' : 'single-recipe-amount'}):
                    for option in select.find_all('option', { 'selected' : 'selected' }):
                        recipe.quantity = int(option.text)

                # Gets the time it takes to make the recipe
                recipe.set_time(r_parse.find("div", {"class" : "recipe-total"}).text)

                # Finds the html with ingredients that also contains unit and amount
                for li in r_parse.find_all('li', {"class" : "components"}):
                    for span in li.find_all('span'): #print(span.text)
                        tempList.append(span.text) #listOfIngredients.append(list.text.replace('\n', ' '))

                # Preprocess ingredients into three seperate lists: item, unit and amount
                for i in range(0, len(tempList), 3):

                    # Normalizes the value to one person/piece
                    if tempList[i] !=  '':
                        recipe.amounts.append(float(tempList[i].replace(',', '.')) / recipe.quantity)
                    else:
                        recipe.amounts.append(None)


                    if (tempList[i + 1] != ''):
                        recipe.units.append(tempList[i + 1])
                    else:
                        recipe.units.append(None)

                    recipe.ingredients.append(tempList[i + 2])

                # Instructions for the recipe
                for div in r_parse.find_all('div', {'class' : 'recipe-procedure'}):
                    for ol in div.find_all('ol'):
                        for li in ol.find_all('li'):
                            recipe.instructions = recipe.instructions + "|"  + li.text

                
                # Type of meal (Dinner, breakfast, etc.)
                for p in r_parse.find_all('p', { 'class' : 'breadcrumbs' }):
                    recipe.set_meal_type(p.text)

                # Unit amount
                for span in r_parse.find_all('span', { 'class' : 'recipe-amount-select'}):
                    recipe.set_amount_unit(span.text)


                recipe.image = str(r_parse.find("div", {'class' : 'recipe-image'})).split('"')[15].split(",")[0].split(" ")[0]
                '''
                print('-----------------------\n', recipe.title)
                for elem in recipe.ingredients:
                    match = editDistance.compute_similarity(elem, match_dict)
                    print(elem + " : " + match)
                '''                
                #database.insertRecipe(title, instructions, image, amountUnit, time, mealType)
                #database.insertIngredients(title, ingredients, units, amounts) 

                '''
                print('\n\nTitle: ' + recipe.title)
                print('Image: ' + recipe.image)
                print('Time: ' + str(recipe.time))
                print('Type: ' + recipe.meal_type)
                print('Unit: ' +  recipe.amount_unit)
                print('--------Ingredients---------')
                
                for i in range(len(recipe.amounts)):
                    print(recipe.amounts[i], recipe.units[i], recipe.ingredients[i])


                print('--------Instructions---------')
                print(recipe.instructions)

                print('-----------------------------')
                '''
                
                database.insert_recipe(recipe)
                print('recipes added: ', x)
                x = x + 1

                sleep(1)
            else:
                sleep(0.1)
        except Exception as e: print(e)

    return recipes

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
recipeScraper(getAllRecipes(urllink1, []))

'''
file = open('rec.txt', 'w', encoding='utf-8')
for key in rec_dict:
    file.write(str(key) + " | " + str(rec_dict[key]) + "\n")

file.close()
'''

#recipeScraper(["https://mummum.dk/medister/i-ovn/"])

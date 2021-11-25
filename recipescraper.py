import requests, database, spacy
from recipe import Recipe
from bs4 import BeautifulSoup
from time import  sleep
from urllib.robotparser import RobotFileParser
from requests.models import Response


def recipe_scraper(urls, match_dict):
    recipes = []
    meal_types = ["Aftensmad", "Frokost", "Søde sager", "Drikkevarer", "Tilbehør til aftensmad", "Sundere alternativer", "Bagværk", "Morgenmad"]
    x = 1

    for url in urls or []:
        try:
            r=requests.get(url)
            r_parse = BeautifulSoup(r.content, "html.parser")

            if r_parse.find('h3', text="Ingrediensliste"):
                recipe = Recipe()
                temp = []
             
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
                        temp.append(span.text) #listOfIngredients.append(list.text.replace('\n', ' '))

                # Preprocess ingredients into three seperate lists: item, unit and amount
                for i in range(0, len(temp), 3):

                    # Normalizes the value to one person/piece
                    if temp[i] !=  '':
                        recipe.amounts.append(float(temp[i].replace(',', '.')) / recipe.quantity)
                    else:
                        recipe.amounts.append(None)


                    if (temp[i + 1] != ''):
                        recipe.units.append(temp[i + 1])
                    else:
                        recipe.units.append(None)

                    recipe.ingredients.append(temp[i + 2])

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


                # Image path
                recipe.image = str(r_parse.find("div", {'class' : 'recipe-image'})).split('"')[15].split(",")[0].split(" ")[0]

                if recipe.meal_type in meal_types:
                    recipes.append(recipe)

                sleep(1)
            else:
                sleep(0.1)
        except Exception as e: print(e)

    database.insert_recipe(recipes, match_dict)

def get_all_recipes(urls, listOfSitesFound):
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
        get_all_recipes(wantToCrawl, listOfSitesFound)

    return listOfSitesFound

rp=RobotFileParser()

nlp = spacy.load('da_core_news_lg')

categories = database.fetch_ingredients()
match_dict = {}
    
for category in categories:
    match_dict[category] = nlp(category.lower())

#Morgen-, Middag-, Aftensmad, og tilbehør til aftensmad
urls = ["https://mummum.dk/opskrifter/"]

recipe_scraper(get_all_recipes(urls, []), match_dict)

#recipe_scraper(['https://mummum.dk/julepavlova-med-kirsebaersauce-og-creme/'])



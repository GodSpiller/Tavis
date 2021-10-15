import pandas as pd
import spacy
from scraper import getAllCatalogs, getTilbud, scraper, recipeScraper, getAllRecipes
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

xl_file = pd.ExcelFile("fixedPrayge.xlsx")
sheet1 = pd.read_excel(xl_file)

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"

nlp = spacy.load('da_core_news_lg')

'''
for vare in getTilbud('7m6-gh4l'):
    temp = 0
    token1 = nlp(vare.lower())
    
    for food in sheet1['Navn'].tolist():

        token2 = nlp(food.lower())

        tempStr = food.split(",")
        if token1.similarity(token2) > temp:
            highestSimilarity = tempStr[0] #sheet1['gruppe'].tolist()[count]
            temp = token1.similarity(token2)
    if temp >= 0.6:
        print("{tilbudsvare} = {fodevare} - {lighed}".format(tilbudsvare = vare, fodevare = highestSimilarity, lighed = temp))
'''
templist = recipeScraper(["https://mummum.dk/spinatroulade-med-laksemousse/"])

print(templist[0])

#for list in templist:

for ingredient in templist[0]:
    #count = 0
    #print(ingredient)
    
    bestSimScore = 0
    bestMatch = ""

    token1 = nlp(ingredient.lower())

    for food in sheet1['Navn'].tolist():

        token2 = nlp(food.lower())

        similarity = token2.similarity(token2)

        if similarity > bestSimScore:
            bestSimScore = similarity
            bestMatch = food
            #print("{ingred} = {fodevare} - {lighed}".format(ingred = ingredient, fodevare = bestMatch, lighed = bestSimScore))

    #for token in token1: #Printer ordtypen på ord i ingredient....... Virker overhovedet ikke....
    #    print(token.text, token.pos_)

    print("{ingred} = {fodevare} - {lighed}".format(ingred = ingredient, fodevare = bestMatch, lighed = bestSimScore))

'''
for ingredient in templist[0]:

    for food in sheet1['Navn'].tolist():
        temp = 0
        bestProduct = ""
        tempStr = food.split(",")        
        for singleIngredient in ingredient:
            boolVar = True
            token1 = nlp(str(singleIngredient))
            token2 = nlp(str(tempStr[0]))

            for token in token1:
                if token.is_oov == True:
                    boolVar = False
            for token in token2:
                if token.is_oov == True:
                    boolVar = False
            #print(boolVar)
            if boolVar == True:
                if token1.similarity(token2) > temp:
                    highestSimilarity = tempStr[0] #sheet1['gruppe'].tolist()[count]
                    bestProduct = singleIngredient
                    temp = token1.similarity(token2)
                    #print(temp)

        if temp >= 0.6:
            print("{tilbudsvare} = {fodevare} - {lighed}".format(tilbudsvare = bestProduct, fodevare = highestSimilarity, lighed = temp))
'''



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

print("Enter two space-separated words")
word1 = input()
word2 = input()
  
token1 = nlp(word1)
token2 = nlp(word2)

print("Similarity:", token1.similarity(token2))

# for vare in getTilbud('7m6-gh4l'):
#     temp = 0
#     #count = 0
    
#     for food in sheet1['Navn'].tolist():
#         tempStr = food.split(",")
#         if similar(tempStr[0], vare) > temp:
#             highestSimilarity = tempStr[0] #sheet1['gruppe'].tolist()[count]
#             temp = similar(tempStr[0], vare)
#         #count += 1
#     if temp >= 0.6:
#         print("{tilbudsvare} = {fodevare} - {lighed}".format(tilbudsvare = vare, fodevare = highestSimilarity, lighed = temp))

""" templist = [recipeScraper(getAllRecipes(urllink2))]

#for list in templist:
for ingredient in templist[40]:
    temp = 0
    #count = 0
    
    for food in sheet1['Navn'].tolist():
        tempStr = food.split(",")
        if similar(tempStr[0], ingredient) > temp:
            highestSimilarity = tempStr[0] #sheet1['gruppe'].tolist()[count]
            temp = similar(tempStr[0], ingredient)
        #count += 1
    if temp >= 0.6:
        print("{tilbudsvare} = {fodevare} - {lighed}".format(tilbudsvare = ingredient, fodevare = highestSimilarity, lighed = temp))
 """



import pandas as pd
from scraper import getAllCatalogs, getTilbud, scraper
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

xl_file = pd.ExcelFile("fixedPrayge.xlsx")
sheet1 = pd.read_excel(xl_file)

urllink = "https://etilbudsavis.dk/discover/groceries"

for vare in getTilbud('7m6-gh4l'):
    temp = 0
    for food in sheet1['Navn'].tolist():
        if similar(food, vare) > temp:
            highestSimilarity = food
            temp = similar(food, vare)
    if temp >= 0.6:
        print("{tilbudsvare} = {fodevare} - {lighed}".format(tilbudsvare = vare, fodevare = highestSimilarity, lighed = temp))

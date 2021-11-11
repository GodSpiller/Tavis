import pandas as pd
import spacy
from discountscraper import getAllCatalogs, getTilbud, scraper
from recipescraper import recipeScraper, getAllRecipes
from difflib import SequenceMatcher

def splitProducts(productName):
    temp = productName
    splitProduct = temp.replace(" eller ", ",").split(",")

    print(productName + " : " + str(splitProduct))

    return splitProduct

def findNouns(productName):
    noun = ""

    for token in nlp(productName.lower()):
        if token.pos_ == 'NOUN':
            if noun == "":
                noun = noun + token.text 
            else:
                noun = (noun + " " + token.text)

    return noun.lower()

def inVocab(tokens):
    for token in tokens:
        if token.is_oov:
            return False
    return True

def computeSimilarities():
    count = 0
    for vare in getTilbud('7m6-gh4l'):
       
        for el in splitProducts(vare):
            similarityScore = 0
            bestMatch = ""
            cleanVare = nlp(findNouns(el))

            for food in sheet1['Navn'].tolist():
                #cleanFood = nlp(food.replace(', rå', '').replace(',', '').lower())
                cleanFood = nlp(food.replace(',', '').lower().split(" ")[0])
                #if inVocab(cleanVare) and inVocab(cleanFood):
                
                tempSim = cleanVare.similarity(cleanFood)

                if tempSim > similarityScore:
                    similarityScore = tempSim
                    bestMatch = cleanFood.text

            print(cleanVare.text + " : " + bestMatch + " similarity = " + str(similarityScore))
            if similarityScore > 0.7:
                #print(cleanVare.text + " : " + bestMatch + " similarity = " + str(similarityScore))
                count += 1
                print(count)
                

nlp = spacy.load('da_core_news_lg')

xl_file = pd.ExcelFile("fixedPrayge.xlsx")
sheet1 = pd.read_excel(xl_file)

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"

computeSimilarities()



        


import pandas as pd
import spacy
from scraper import getAllCatalogs, getTilbud, scraper, recipeScraper, getAllRecipes
from difflib import SequenceMatcher

def findNouns(productName):
    temp = productName.text
    splitProduct = []
    if "," in temp:
        t1 = temp.split(",")
        splitProduct.append(t1)
        for n in splitProduct:
            if "eller" in n:
                splitProduct.remove(n)
                splitProduct.append(n.split('eller'))
    elif "eller" in temp:
        splitProduct.append(temp.split("eller"))
    
    print(productName.text + " : " + str(splitProduct))

    nounIndices = ""
    for token in productName:
        if token.pos_ == 'NOUN' or token.pos == 'PROPN':
            nounIndices = nounIndices + " " + token.text
            
    return nounIndices
        #print(productName.text + " : " + token.text, token.dep_, token.head.text, token.head.pos_, [child for child in token.children])

def inVocab(tokens):
    for token in tokens:
        if token.is_oov:
            return False
    return True

def computeSimilarities():
    for vare in getTilbud('7m6-gh4l'):
        similarityScore = 0

        cleanVare = nlp(findNouns(nlp(vare)).lower()) 
        bestMatch = ""

        
        for food in sheet1['Navn'].tolist():
            cleanFood = nlp(food.replace(', rå', '').replace(',', '').lower())

            #if inVocab(cleanVare) and inVocab(cleanFood):
            tempSim = cleanVare.similarity(cleanFood)

            if tempSim > similarityScore:
                similarityScore = tempSim
                bestMatch = cleanFood.text
        if similarityScore > 0.7:
            print(cleanVare.text + " : " + bestMatch + " similarity = " + str(similarityScore))

nlp = spacy.load('da_core_news_lg')

xl_file = pd.ExcelFile("fixedPrayge.xlsx")
sheet1 = pd.read_excel(xl_file)

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"

computeSimilarities()



        


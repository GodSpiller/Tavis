import pandas as pd
import spacy
from discountscraper import getAllCatalogs, scraper
from difflib import SequenceMatcher

'''def splitProducts(productName):
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
  '''              

def compute_similarity(ingredient, categories):
    ingredient = nlp(ingredient.lower())
    similarity_score = 0
    best_match = ""

    for key in categories:
        

        whole_similarity = ingredient.similarity(categories[key])
        first_word_similarity = ingredient.similarity(categories[key][0])

        if whole_similarity > first_word_similarity:
            if whole_similarity > similarity_score:
                similarity_score = whole_similarity
                best_match = key
        else:
            if first_word_similarity > similarity_score:
                similarity_score = first_word_similarity
                best_match = key
        
    return best_match

nlp = spacy.load('da_core_news_lg')
'''
xl_file = pd.ExcelFile("fixedPrayge.xlsx")
sheet1 = pd.read_excel(xl_file)

urllink = "https://etilbudsavis.dk/discover/groceries"
urllink2 = "https://mummum.dk/opskrifter/aftensmad/"
'''





        


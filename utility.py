import spacy
import operator
from collections import OrderedDict
nlp = spacy.load('da_core_news_lg')

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
    if similarity_score > 0.8:
        return best_match

def convertToMinutes(input):
    arr = input.split(' ')
    arr = list(filter(None, arr))

    if (len(arr) == 2):
        return int(arr[0])
    else:
        return int(arr[0]) * 60 + int(arr[3])



def compute_similarity_discount(discount, categories, offer_amount):
    discount = nlp(discount.lower())
    similarity_score = 0
    best_match = []
    similarity_dict = {}

    nouninized_discount = ""

    for token in discount:
        if token.pos_ == 'NOUN':
            nouninized_discount += " " + token.text

    nouninized_discount = nlp(nouninized_discount)

    for key in categories:    
        similarity = nouninized_discount.similarity(categories[key])
        similarity_dict[key] = similarity

        if similarity > similarity_score:
            similarity_score = similarity
            best_match = key    

    if offer_amount > 1:
        return highest_values(similarity_dict, offer_amount)
    elif similarity_score > 0.85:
        return best_match


def highest_values(dict, offer_amount):
    sorted_fun = sorted(dict.items(), key=operator.itemgetter(1))
    dumb_list = []
    top_list = []

    sorted_dict = OrderedDict()
    for k, v in sorted_fun:
        sorted_dict[k] = v

    for key in sorted_dict.keys():
        dumb_list.append([key, sorted_dict[key]])
    
    dumb_list.reverse()

    for x in range(offer_amount):
        if dumb_list[x][1] > 0.85:
            top_list.append(dumb_list[x])
    return top_list
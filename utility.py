import spacy
import operator

nlp = spacy.load('da_core_news_lg')

def compute_similarity(ingredient, categories):
    ingredient = nlp(ingredient.lower())
    similarity_score = 0
    best_match = ""

    for key in categories:    
        similarity = ingredient.similarity(categories[key])

        if similarity > similarity_score:
            similarity_score = similarity
            best_match = key

    if similarity_score > 0.8:
        return best_match

def compute_similarity_discount(discount, categories, offer_amount):
    discount = nlp(discount)
    similarity_score = 0
    best_match = []
    similarity_dict = {}
    nouninized_discount = ""

    for token in discount:
        if token.pos_ == 'NOUN':
            nouninized_discount += " " + token.text

    nouninized_discount = nlp(nouninized_discount.lower())

    for key in categories:    
        similarity = nouninized_discount.similarity(categories[key])
        similarity_dict[key] = similarity

        if similarity > similarity_score:
            similarity_score = similarity
            best_match = key    

    if offer_amount > 1:
        return highest_values(similarity_dict, offer_amount)
    elif similarity_score > 0.85:
        return [(best_match, similarity_score)]


def highest_values(dict, offer_amount):
    sorted_similarities = sorted(dict.items(), key=operator.itemgetter(1))
    best_matches = []

    sorted_similarities.reverse()

    for x in range(offer_amount):
        if sorted_similarities[x][1] > 0.85:
            best_matches.append(sorted_similarities[x])

    return best_matches
    

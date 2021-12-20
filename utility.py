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

def compute_similarity_discount(discount, categories, product_count):
    discount = nlp(discount)
    similarity_score = 0
    best_match = []
    similarities = {}
    discount_nouns = ""

    for token in discount:
        if token.pos_ == 'NOUN':
            discount_nouns += " " + token.text

    discount_nouns = nlp(discount_nouns.lower())

    for key in categories:    
        similarity = discount_nouns.similarity(categories[key])
        similarities[key] = similarity

        if similarity > similarity_score:
            similarity_score = similarity
            best_match = key    

    if product_count > 1:
        return highest_values(similarities, product_count)
    elif similarity_score > 0.85:
        return [(best_match, similarity_score)]


def highest_values(dict, product_count):
    sorted_similarities = sorted(dict.items(), key=operator.itemgetter(1))
    best_matches = []

    sorted_similarities.reverse()

    for x in range(product_count):
        if sorted_similarities[x][1] > 0.85:
            best_matches.append(sorted_similarities[x])

    return best_matches

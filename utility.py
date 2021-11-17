import spacy   
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
        
    return best_match

def convertToMinutes(input):
    arr = input.split(' ')
    arr = list(filter(None, arr))

    if (len(arr) == 2):
        return int(arr[0])
    else:
        return int(arr[0]) * 60 + int(arr[3])
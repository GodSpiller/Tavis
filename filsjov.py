import database, spacy

file = open('rec.txt', 'r', encoding='utf-8')

lines = file.readlines()

list_of_trash = []

for line in lines:
    temp = line.split('|')
    ratio = temp[1]
    ing_cat = temp[0].split(' : ')
    
    list_of_trash.append(
        {'ingredient' : ing_cat[0], 
        'category' : ing_cat[1], 
        'recurrence' : int(ratio)})

def get_recurrence(trash):
    return trash.get('recurrence')

list_of_trash.sort(key=get_recurrence)
list_of_trash.reverse()

nlp = spacy.load('da_core_news_lg')
hej = ['hel', 'lys', 'mørk', 'frossen', 'frosne', 'frisk', 'sød', 'rød', 'gul', 'grøn']            

for element in list_of_trash:
    temp = nlp(element.get('ingredient'))   
    if len(temp) > 1:
        for token in temp:
            if token.text in hej:
                print(temp.text)
                
                
                #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                #token.shape_, token.is_alpha, token.is_stop)


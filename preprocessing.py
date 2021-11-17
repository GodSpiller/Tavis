import database, spacy

file = open('rec.txt', 'r', encoding='utf-8')

lines = file.readlines()

raw_ingredients = []

for line in lines:
    temp = line.split('|')
    ratio = temp[1]
    ing_cat = temp[0].split(' : ')
    
    raw_ingredients.append(
        {'ingredient' : ing_cat[0], 
        'category' : ing_cat[1], 
        'recurrence' : int(ratio)})

def get_recurrence(trash):
    return trash.get('recurrence')

raw_ingredients.sort(key=get_recurrence)
raw_ingredients.reverse()

nlp = spacy.load('da_core_news_lg')
hej = ['hel', 'lys', 'mørk', 'frossen', 'frosne', 'frisk', 'sød', 'rød', 'gul', 'grøn']            

def process_ingredients():
    ingredients = []

    for i in raw_ingredients:
        if i.get('ingredient') not in ingredients:
            ingredients.append(i.get('ingredient'))

    for i in ingredients:
        database.insert_ingredient_category(i)
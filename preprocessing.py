import database

def get_recurrence(ingredient):
    return ingredient.get('recurrence')

def process_ingredients():
    ingredients = []
    
    for i in ingredients:
        database.insert_ingredient_category(i)


newfile = open('newrec.txt', 'r', encoding='utf-8')

lines = newfile.readlines()

ingredients = []

for line in lines:
    ingredients.append(line) 

database.insert_ingredient_category(ingredients)

#raw_ingredients.sort(key=get_recurrence)
#raw_ingredients.reverse()

#process_ingredients()
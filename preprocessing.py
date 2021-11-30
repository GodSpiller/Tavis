import database

def process_ingredients():
    newfile = open('newrec.txt', 'r', encoding='utf-8')
    lines = newfile.readlines()
    ingredients = []

    for line in lines:
        ingredients.append(line) 

    database.insert_ingredient_category(ingredients)


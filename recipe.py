import recipescraper, database

def insertRecipes():
    conn = database.connectToDB()
    curs = conn.cursor()

    for index, row in df.iterrows():
        group = row['gruppe']
        name = row['Navn']
        curs.execute('INSERT INTO food_category (supercategory_id, title) VALUES((SELECT id FROM food_supercategory WHERE title = \'%s\'), \'%s\')' % (group, name))
        conn.commit()

    curs.close()
    conn.close()
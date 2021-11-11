import database
import pandas as pd

xl_file = pd.ExcelFile("fixedPrayge.xlsx")
df = pd.read_excel(xl_file)


# Inserts data into food_supercategory with the group name
def insertSuperCategories():
    conn = database.connectToDB()
    curs = conn.cursor()

    alreadyUsed = []

    for index, row in df.iterrows():
        group = row['gruppe']

        if group not in alreadyUsed:
            curs.execute('INSERT INTO food_supercategory (title) VALUES(\'%s\')' % group)
            conn.commit()
            alreadyUsed.append(group)

    curs.close()
    conn.close()

# Inserts data to the food_category table with the name of the products
# and the foreign key corresponding to the group
def insertCategories():
    conn = database.connectToDB()
    curs = conn.cursor()

    for index, row in df.iterrows():
        group = row['gruppe']
        name = row['Navn']
        curs.execute('INSERT INTO food_category (supercategory_id, title) VALUES((SELECT id FROM food_supercategory WHERE title = \'%s\'), \'%s\')' % (group, name))
        conn.commit()

    curs.close()
    conn.close()
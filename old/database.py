import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder

def connectToDB():
    try:
        print('Connecting to the PostgreSQL Database...')
        '''
        ssh_tunnel = SSHTunnelForwarder(
            ('10.92.0.161', 22),
            ssh_username="ubuntu",
            ssh_private_key= 'SSHKEY.pem',
            remote_bind_address=('localhost', 5432)
        )

        ssh_tunnel.start()  
        
        '''

        conn = pg.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='andreas',
            database='localtavis'
        )

    except:
        print('Connection Has Failed...') 
    
    return conn

#curs.execute('INSERT INTO food_category (supercategory_id, title) VALUES((SELECT id FROM food_supercategory WHERE title = \'%s\'), \'%s\')' % (group, name))

def insertRecipe(title, instructions, img, amount_unit, time, meal_type):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute('INSERT INTO recipe (title, instructions, time, amount_unit, meal_type, image_file_path) VALUES(\'%s\', \'%s\', %d, \'%s\', \'%s\', \'%s\')' % (title, instructions, time, amount_unit, meal_type, img))
    conn.commit()

    curs.close()
    conn.close()


def insertIngredients(recipe_title, ingredients, units, amounts):
    conn = connectToDB()
    curs = conn.cursor()

    for i in len(ingredients):

        curs.execute('INSERT INTO ingredient (category, recipe_id, title, amount, unit) ')

    curs.close()
    conn.close()

def fetch_categories():
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute('SELECT title FROM food_category')
    result = curs.fetchall()

    categories = map(list, list(result))
    categories = sum(categories, [])

    curs.close()
    conn.close()

    return categories


def fetch_super_category(super_category):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute("SELECT title FROM food_supercategory WHERE title = '%s'" % (super_category))
    result = curs.fetchall()

    curs.close()
    conn.close()

    return result


def insert_category(title, super_category):
    conn = connectToDB()
    curs = conn.cursor()
    
    if fetch_super_category(super_category):
        curs.execute('INSERT INTO food_category (supercategory_id, title) VALUES((SELECT id FROM food_supercategory WHERE title = \'%s\'), \'%s\')' % (super_category, title))
        conn.commit()
    else:
        curs.execute('INSERT INTO food_supercategory (title) VALUES(\'%s\')' % super_category)
        conn.commit()
        curs.execute('INSERT INTO food_category (supercategory_id, title) VALUES((SELECT id FROM food_supercategory WHERE title = \'%s\'), \'%s\')' % (super_category, title))
        conn.commit()

    curs.close()
    conn.close()


    


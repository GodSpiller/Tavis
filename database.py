import utility
import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder
from recipe import Recipe

def connectToDB():
    try:
        
        ssh_tunnel = SSHTunnelForwarder(
            ('10.92.0.161', 22),
            ssh_username="ubuntu",
            ssh_private_key= 'SSHKEY.pem',
            remote_bind_address=('localhost', 5432)
        )

        ssh_tunnel.start()  
        

        conn = pg.connect(
            host='localhost',
            port=ssh_tunnel.local_bind_port, # REPLACE WITH 'ssh_tunnel.local_bind_port' WHEN SSH
            user='postgres', # CHANGE WHEN INSERTING TO VM
            password='tavis', # CHANGE WHEN INSERTING TO VM
            database='tavis' # CHANGE WHEN INSERTING TO VM
        )

    except:
        print('Connection Has Failed...') 
    
    return conn

def insert_recipe(recipe, match_dict):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute(
        '''
        INSERT INTO
            recipe_types (type) 
        VALUES
            (%s)
        ON CONFLICT DO NOTHING
        ''', (recipe.meal_type,)
    )

    conn.commit()

    curs.execute(
        '''
        SELECT 
            id 
        FROM 
            recipe_types 
        WHERE 
            type=%s
        ''', (recipe.meal_type,)
    )

    type_query = curs.fetchone()[0]

    curs.execute(
        '''
        INSERT INTO 
            recipes (title, instructions, time, amount_unit, type_id, image_file_path)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        ''', (recipe.title, recipe.instructions, recipe.time, recipe.amount_unit, type_query, recipe.image,)
    )

    conn.commit()

    curs.execute(
        '''
        SELECT 
            id 
        FROM 
            recipes
        WHERE 
            title=%s
        ''', (recipe.title,)
    )

    recipe_query = curs.fetchone()[0]

    for i in range(len(recipe.ingredients)):

        match = utility.compute_similarity(recipe.ingredients[i], match_dict)

        curs.execute(
            '''
            SELECT
                id
            FROM
                food_supercategories
            WHERE
                title=%s                
            ''', (match,)
        )
        
        category_query = curs.fetchone()[0]

        curs.execute(
            '''
            INSERT INTO
                ingredients (category, recipe_id, amount, unit)
            VALUES
                (%s, %s, %s, %s)                
            ''', (category_query, recipe_query, recipe.amounts[i], recipe.units[i],)
        )
        conn.commit()

    curs.close()
    conn.close()


def insert_ingredient_category(ingredient):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute(
        '''
        INSERT INTO
            food_supercategories (title)
        VALUES
            (%s)
        ''', (ingredient,)
    )

    conn.commit()

    curs.close()
    conn.close()

def fetch_ingredients():
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute(
        '''
        SELECT
            title
        FROM
            food_supercategories
        '''
    )

    result = curs.fetchall()

    categories = map(list, list(result))
    categories = sum(categories, [])

    curs.close()
    conn.close()

    return categories
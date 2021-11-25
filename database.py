import utility
import psycopg2 as psycopg2
import psycopg2.extras as extras
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

        conn = psycopg2.connect(
            host='localhost',
            port=ssh_tunnel.local_bind_port, # REPLACE WITH 'ssh_tunnel.local_bind_port' WHEN SSH
            user='postgres', # CHANGE WHEN INSERTING TO VM
            password='tavis', # CHANGE WHEN INSERTING TO VM
            database='tavis_new' # CHANGE WHEN INSERTING TO VM
        )

    except:
        print('Connection Has Failed...') 

    return conn

def insert_recipe(recipes, match_dict):
    conn = connectToDB()
    curs = conn.cursor()
    
    for recipe in recipes:
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
            if match != None:
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


def fetch_catalogue_id():
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute(''' SELECT id FROM discount_catalogues''')
    
    result = curs.fetchall()
    catalogue_ids = map(list, list(result))
    catalogue_ids = sum(catalogue_ids, [])

    curs.close()
    conn.close()

    return catalogue_ids


def insert_catalogue(catalogue):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute(
    '''
    INSERT INTO discount_catalogues (store_chain_id, valid_from, valid_to, id)
        SELECT 
            s.id,
            TO_DATE(%s , 'YYYY/MM/DD'),
            TO_DATE(%s , 'YYYY/MM/DD'),
            %s
        FROM
            store_chains as s
        WHERE
            s.name = %s AND
            NOT EXISTS 
                (SELECT
                    *
                FROM
                    discount_catalogues as d
                WHERE d.id = %s)
                ON CONFLICT DO NOTHING
            
    ''', (catalogue.valid_from, catalogue.valid_to, catalogue.catalogue_id, catalogue.store_name, catalogue.catalogue_id,))

    conn.commit()
    curs.close()
    conn.close()
    
    
def insert_discount_product(discount):
    conn = connectToDB()
    
    tuples = [tuple(x) for x in discount]
    print(tuples)
    # SQL quert to execute
    query  = '''INSERT INTO discount_products 
                    (catalogue_id, title, price, valid_from, valid_to, unit, amount) 
                VALUES 
                    %%s''' % ()
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()
    conn.close()


def batch_insert_matches(discounts):
    conn = connectToDB()
    curs = conn.cursor()
    
    for discount in discounts:
        if discount.matches != None:
            for match in discount.matches:
                curs.execute('''INSERT INTO product_category (discount_product_id, food_supercategory_id, match_ratio)
                        SELECT
                            discount_products.id,
                            food_supercategories.id,
                            %s
                        FROM 
                            discount_products, food_supercategories
                        WHERE
                            discount_products.title = %s AND
                            food_supercategories.title = %s
                    ''', (match[1], discount.title, match[0],))
    conn.commit()

    curs.close()
    conn.close()
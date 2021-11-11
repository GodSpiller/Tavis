import psycopg2 as pg
from sshtunnel import SSHTunnelForwarder

def connectToDB():
    try:
        print('Connecting to the PostgreSQL Database...')

        ssh_tunnel = SSHTunnelForwarder(
            ('10.92.0.161', 22),
            ssh_username="ubuntu",
            ssh_private_key= 'SSHKEY.pem',
            remote_bind_address=('localhost', 5432)
        )

        ssh_tunnel.start()  
        
        conn = pg.connect(
            host='localhost',
            port=ssh_tunnel.local_bind_port,
            user='postgres',
            password='tavis',
            database='tavis2'
        )

    except:
        print('Connection Has Failed...') 
    
    return conn

def insertRecipe(title, ingredients, units, amounts, instructions, img):
    conn = connectToDB()
    curs = conn.cursor()

    curs.execute('INSERT INTO ')

    curs.close()
    conn.close()
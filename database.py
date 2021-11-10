import psycopg2
from sshtunnel import SSHTunnelForwarder

try:
    with SSHTunnelForwarder(
         ('10.92.0.161', 22),
         ssh_private_key="SSHKey.pem",
         ssh_username="ubuntu",
         remote_bind_address=('localhost', 5432)) as server:
         
         server.start()
         print("server connected")

         print(server.local_bind_port)
         params = {
             'database': 'tavis',
             'user': 'postgres',
             'password': 'tavis',
             'host': 'localhost',
             'port': server.local_bind_port
             }

         conn = psycopg2.connect(**params)
         curs = conn.cursor()
         curs.execute('SELECT * FROM chains')
         for row in curs.fetchall():
             print(row[1])

         print("database connected")

except:
    print("Connection Failed")



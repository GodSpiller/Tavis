import psycopg2
from sshtunnel import SSHTunnelForwarder

def connectToDb():
    try:
        with SSHTunnelForwarder(
            ('10.92.0.161', 22),
            ssh_private_key="SSHKey.pem",
            ssh_username="ubuntu",
            remote_bind_address=('localhost', 5432)) as server:
            
            server.start()
            print("server connected")

            print(server.local_bind_port)
            conn = psycopg2.connect(
                host = 'localhost',
                port = server.local_bind_port,
                user = 'postgres',
                password = 'tavis',
                database = 'tavis')
                
            return conn
          
    except:
        print("Connection Failed")




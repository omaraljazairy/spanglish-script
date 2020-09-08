import psycopg2
from config import DB

def dbconn():
    """ opens a db connection and returns a connection object"""

    try:
        conn = psycopg2.connect(host=DB['host'],database=DB['database'], user=DB['username'], password=DB['password'])
        print("connection successfully opened")
        return conn
    except Exception as e:
        print("error opening db connection: ", e)
        exit("try reconnecting again")


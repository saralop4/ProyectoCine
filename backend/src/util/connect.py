from sqlite3 import Error
import sqlite3
import os

path = './src/db/cine.db'
db_url  = os.path.abspath(path)

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_url)
    except Error as e:
        print(e)

    return conn

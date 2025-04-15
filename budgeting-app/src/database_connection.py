import os
import sqlite3

dirname = os.path.dirname(__file__)
database_file = os.path.join(dirname, "..", "data", "database.db")

connection = None


def get_database_connection():
    global connection

    data_dir = os.path.join(dirname, "..", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if connection is None:
        connection = sqlite3.connect(database_file)
        connection.row_factory = sqlite3.Row

    return connection

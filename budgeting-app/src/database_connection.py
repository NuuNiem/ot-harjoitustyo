import os
import sqlite3

dirname = os.path.dirname(__file__)
database_file = os.path.join(dirname, "..", "data", "database.db")

_connection = None

def get_database_connection():
    global _connection
    
    data_dir = os.path.join(dirname, "..", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    if _connection is None:
        _connection = sqlite3.connect(database_file)
        _connection.row_factory = sqlite3.Row
    
    return _connection
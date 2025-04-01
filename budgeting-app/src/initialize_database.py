from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS budgets")
    cursor.execute("DROP TABLE IF EXISTS users")
    connection.commit()

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        '''
    )
    connection.commit()

def initialize_database():
    connection = get_database_connection()

    #drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
from database_connection import get_database_connection


def drop_tables(connection):
    """Poistaa tietokantataulut.
    
    Args:
        connection: = Tietokantayhteyden Connection-olio.
    """
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS expenses")
    cursor.execute("DROP TABLE IF EXISTS budgets")
    cursor.execute("DROP TABLE IF EXISTS users")
    connection.commit()


def create_tables(connection):
    """Luo tietokantataulut.

    Args:
        connection: Tietokantayhteyden Connection-olio.
    """
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_amount REAL NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            budget_id INTEGER NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budgets (id)
        )
    ''')

    connection.commit()


def initialize_database():
    """Alustaa tietokantataulut."""
    connection = get_database_connection()

    # drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()

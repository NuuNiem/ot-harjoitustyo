from entities.user import User
from database_connection import get_database_connection


class UserRepository:
    def __init__(self, connection=get_database_connection()):
        self._connection = connection

    def create(self, username, password=""):
        cursor = self._connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self._connection.commit()

            return User(username)
        except Exception as exc:
            self._connection.rollback()
            raise ValueError(f"Username '{username}' already exists") from exc

    def find_by_username(self, username):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (username,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return User(row["username"])

    def find_all(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT username FROM users")
        rows = cursor.fetchall()

        return [User(row["username"]) for row in rows]

    def delete_all(self):
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM users")

        self._connection.commit()


user_repository = UserRepository()

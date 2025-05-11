from entities.user import User
from database_connection import get_database_connection


class UserRepository:
    """Käyttäjiin liittyvistä tietokantaoperaatioista vastaava luokka.
    """

    def __init__(self, connection=get_database_connection()):
        """Luokan konstruktori.

        Args:
            connection: Tietokantayhteyden Connection-olio.
        """
        self._connection = connection

    def create(self, username, password=""):
        """Tallentaa uuden käyttäjän tietokantaan.

        Args:
            username: Käyttäjän käyttäjätunnus.
            password: Käyttäjän salasana.

        Returns:
            Tallennettu käyttäjä User-oliona.

        Raises:
            ValueError: Jos käyttäjätunnus on jo olemassa.
        """
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self._connection.commit()
            return User(username, password)
        except Exception as exc:
            self._connection.rollback()
            raise ValueError(f"Username '{username}' already exists") from exc

    def find_by_username(self, username, password=None):
        """Palauttaa käyttäjän käyttäjätunnuksen (ja tarvittaessa salasanan) perusteella.

        Args:
            username: Käyttäjätunnus.
            password: (Vapaaehtoinen) Käyttäjän salasana.

        Returns:
            User-olio, jos käyttäjä löytyy, muuten None.
        """
        cursor = self._connection.cursor()
        if password is not None:
            cursor.execute(
                "SELECT username, password FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
        else:
            cursor.execute(
                "SELECT username, password FROM users WHERE username = ?",
                (username,)
            )
        row = cursor.fetchone()
        if not row:
            return None
        return User(row["username"], row["password"])

    def find_all(self):
        """Palauttaa kaikki käyttäjät.

        Returns:
            Lista User-olioita.
        """
        cursor = self._connection.cursor()

        cursor.execute("SELECT username, password FROM users")
        rows = cursor.fetchall()

        return [User(row["username"], row["password"]) for row in rows]

    def delete_all(self):
        """Poistaa kaikki käyttäjät tietokannasta.
        """
        cursor = self._connection.cursor()

        cursor.execute("DELETE FROM users")

        self._connection.commit()


user_repository = UserRepository()

from entities.budgeting import Budgeting
from entities.expense import Expense
from database_connection import get_database_connection


class BudgetRepository:
    """Budjetteihin liittyvistä tietokantaoperaatioista vastaava luokka."""

    def __init__(self, connection=get_database_connection()):
        """Luokan konstruktori.

        Args:
            connection: Tietokantayhteyden Connection-olio.
        """
        self._connection = connection

    def create(self, budget_name, total_amount, username):
        """Luo uuden budjetin tietokantaan.

        Args:
            budget_name: Budjetin nimi.
            total_amount: Budjetin kokonaissumma.
            username: Käyttäjän käyttäjätunnus, jolle budjetti kuuluu.

        Returns:
            Luotu Budgeting-olio.

        Raises:
            ValueError: Jos käyttäjää ei löydy.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )
        user_row = cursor.fetchone()
        if not user_row:
            raise ValueError(f"User '{username}' not found")
        cursor.execute(
            "INSERT INTO budgets (name, total_amount, user_id) VALUES (?, ?, ?)",
            (budget_name, total_amount, user_row["id"])
        )
        self._connection.commit()
        budget_id = cursor.lastrowid
        return Budgeting(budget_name, total_amount, budget_id)

    def find_all_by_username(self, username):
        """Palauttaa kaikki käyttäjän budjetit.

        Args:
            username: Käyttäjän käyttäjätunnus.

        Returns:
            Lista Budgeting-olioita.
        """
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT b.id, b.name, b.total_amount, 
                   SUM(COALESCE(e.amount, 0)) AS spent_amount
            FROM budgets b
            LEFT JOIN users u ON b.user_id = u.id
            LEFT JOIN expenses e ON e.budget_id = b.id
            WHERE u.username = ?
            GROUP BY b.id
        ''', (username,))
        rows = cursor.fetchall()
        return [self._row_to_budget(row) for row in rows]

    def get_budget_by_id(self, budget_id):
        """Palauttaa budjetin id:n perusteella.

        Args:
            budget_id: Budjetin tunniste.

        Returns:
            Budgeting-olio, jos löytyy, muuten None.
        """
        cursor = self._connection.cursor()
        cursor.execute('''
            SELECT b.id, b.name, b.total_amount, 
                SUM(COALESCE(e.amount, 0)) AS spent_amount
            FROM budgets b
            LEFT JOIN expenses e ON e.budget_id = b.id
            WHERE b.id = ?
            GROUP BY b.id
        ''', (budget_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_budget(row)

    def get_budget_expenses(self, budget_id):
        """Palauttaa kaikki budjettiin liittyvät kulut.

        Args:
            budget_id: Budjetin tunniste.

        Returns:
            Lista Expense-olioita.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, description, amount FROM expenses WHERE budget_id = ?",
            (budget_id,)
        )
        expenses = cursor.fetchall()
        return [Expense(
            expense["description"],
            expense["amount"],
            expense["id"],
            budget_id
        ) for expense in expenses]

    def _row_to_budget(self, row):
        """Muuttaa tietokantarivin Budgeting-olioksi.

        Args:
            row: Tietokantarivi.

        Returns:
            Budgeting-olio.
        """
        budget = Budgeting(row["name"], row["total_amount"], row["id"])
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT description, amount FROM expenses WHERE budget_id = ?",
            (row["id"],)
        )
        expenses = cursor.fetchall()
        for expense in expenses:
            budget.expenses.append((expense["description"], expense["amount"]))
        return budget

    def add_expense(self, budget_id, description, amount):
        """Lisää uuden kulun budjettiin.

        Args:
            budget_id: Budjetin tunniste.
            description: Kulun kuvaus.
            amount: Kulun määrä.

        Raises:
            ValueError: Jos budjettia ei löydy tai kulun määrä ylittää budjetin.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT total_amount FROM budgets WHERE id = ?",
            (budget_id,)
        )
        budget_row = cursor.fetchone()
        if not budget_row:
            raise ValueError(f"Budget with id {budget_id} not found")
        cursor.execute(
            "SELECT SUM(amount) as total_spent FROM expenses WHERE budget_id = ?",
            (budget_id,)
        )
        amount = float(amount) if isinstance(amount, str) else amount
        spent_row = cursor.fetchone()
        spent_amount = spent_row[0] if spent_row[0] else 0
        remaining = budget_row["total_amount"] - spent_amount
        if remaining < amount:
            raise ValueError("Expense amount exceeds budget")
        cursor.execute(
            "INSERT INTO expenses (description, amount, budget_id) VALUES (?, ?, ?)",
            (description, amount, budget_id)
        )

    def remove_expense(self, expense_id):
        """Poistaa kulun budjetista.

        Args:
            expense_id: Kulun tunniste.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

    def remove_budget(self, budget_id):
        """Poistaa budjetin ja siihen liittyvät kulut.

        Args:
            budget_id: Budjetin tunniste.
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE budget_id = ?",
            (budget_id,)
        )
        cursor.execute(
            "DELETE FROM budgets WHERE id = ?",
            (budget_id,)
        )
        self._connection.commit()

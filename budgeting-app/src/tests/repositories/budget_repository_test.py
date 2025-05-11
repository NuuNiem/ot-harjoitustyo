import unittest
import sqlite3
from repositories.budget_repository import BudgetRepository
from entities.budgeting import Budgeting


class TestBudgetRepository(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.repo = BudgetRepository(self.connection)
        self._create_tables()

        self.connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", ("kayttaja", "666"))
        self.connection.commit()

    def _create_tables(self):
        self.connection.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            );
        """)
        self.connection.execute("""
            CREATE TABLE budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                total_amount REAL,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
        """)
        self.connection.execute("""
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                amount REAL,
                budget_id INTEGER,
                FOREIGN KEY(budget_id) REFERENCES budgets(id)
            );
        """)

    def test_create_budget_success(self):
        budget = self.repo.create("Ruoka", 100.0, "markku")
        self.assertIsInstance(budget, Budgeting)
        self.assertEqual(budget.name, "Ruoka")
        self.assertEqual(budget.total_amount, 100.0)

    def test_create_budget_user_not_found(self):
        with self.assertRaises(ValueError):
            self.repo.create("Ruoka", 100.0, "ei_ole")

    def test_find_all_by_username(self):
        self.repo.create("Ruoka", 100.0, "markku")
        self.repo.create("Viihde", 50.0, "markku")
        budgets = self.repo.find_all_by_username("markku")
        self.assertEqual(len(budgets), 2)
        names = [b.name for b in budgets]
        self.assertIn("Ruoka", names)
        self.assertIn("Viihde", names)

    def test_get_budget_by_id_and_not_found(self):
        budget = self.repo.create("Ruoka", 100.0, "markku")
        found = self.repo.get_budget_by_id(budget.id)
        self.assertIsNotNone(found)
        not_found = self.repo.get_budget_by_id(999)
        self.assertIsNone(not_found)

    def test_add_expense_and_limit(self):
        budget = self.repo.create("Ruoka", 100.0, "markku")
        self.repo.add_expense(budget.id, "Kauppa", 30.0)
        with self.assertRaises(ValueError):
            self.repo.add_expense(budget.id, "Iso ostos", 100.0)
        with self.assertRaises(ValueError):
            self.repo.add_expense(999, "Testi", 10.0)

    def test_get_budget_expenses(self):
        budget = self.repo.create("Ruoka", 100.0, "markku")
        self.repo.add_expense(budget.id, "Kauppa", 20.0)
        expenses = self.repo.get_budget_expenses(budget.id)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0].description, "Kauppa")

    def test_remove_expense_and_budget(self):
        budget = self.repo.create("Ruoka", 100.0, "markku")
        self.repo.add_expense(budget.id, "Kauppa", 20.0)
        expenses = self.repo.get_budget_expenses(budget.id)
        self.repo.remove_expense(expenses[0].id)
        self.assertEqual(len(self.repo.get_budget_expenses(budget.id)), 0)
        self.repo.remove_budget(budget.id)
        self.assertIsNone(self.repo.get_budget_by_id(budget.id))

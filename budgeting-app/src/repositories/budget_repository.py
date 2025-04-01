from entities.budgeting import Budgeting
from database_connection import get_database_connection

class BudgetRepository:
    def __init__(self, connection=get_database_connection()):
        self._connection = connection
    
    def create(self, budget_name, total_amount, username):
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
        
        return Budgeting(budget_name, total_amount)
    
    def find_all_by_username(self, username):
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
    
    def _row_to_budget(self, row):
        budget = Budgeting(row["name"], row["total_amount"])
        
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
        
        spent_row = cursor.fetchone()
        spent_amount = spent_row[0] if spent_row[0] else 0
        
        remaining = budget_row["total_amount"] - spent_amount
        
        if remaining < amount:
            raise ValueError("Expense amount exceeds budget")
        
        cursor.execute(
            "INSERT INTO expenses (description, amount, budget_id) VALUES (?, ?, ?)",
            (description, amount, budget_id)
        )
        
        self._connection.commit()
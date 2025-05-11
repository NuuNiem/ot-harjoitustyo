from repositories.user_repository import UserRepository
from repositories.budget_repository import BudgetRepository


class BudgetingService:
    def __init__(self):
        self._user_repository = UserRepository()
        self._budget_repository = BudgetRepository()
        self._current_user = None

    def register_user(self, username, password=""):
        return self._user_repository.create(username, password)

    def get_user(self, username, password=None):
        user = self._user_repository.find_by_username(username, password)
        if not user:
            raise ValueError("User not found or password incorrect")
        self._current_user = username
        return user

    def validate_and_create_budget(self, username, name, amount_str):
        if not name:
            raise ValueError("Budget name cannot be empty")

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Budget amount must be positive")

            return self.add_budget_to_user(username, name, amount)
        except ValueError as e:
            if "could not convert string to float" in str(e).lower():
                raise ValueError(
                    "Invalid amount format. Please enter a number.") from e
            raise

    def add_expense(self, budget_id, description, amount):
        return self._budget_repository.add_expense(budget_id, description, amount)

    def add_budget_to_user(self, username, name, amount):
        return self._budget_repository.create(name, amount, username)

    def get_user_budgets(self, username):
        return self._budget_repository.find_all_by_username(username)

    def get_budget_by_id(self, budget_id):
        return self._budget_repository.get_budget_by_id(budget_id)

    def get_budget_expenses(self, budget_id):
        return self._budget_repository.get_budget_expenses(budget_id)

    def get_budget_data_for_display(self, username):
        budgets = self.get_user_budgets(username)
        budget_map = {budget.name: budget for budget in budgets}

        return budgets, budget_map

    def remove_expense(self, expense_id):
        return self._budget_repository.remove_expense(expense_id)

    def remove_budget(self, budget_id):
        return self._budget_repository.remove_budget(budget_id)

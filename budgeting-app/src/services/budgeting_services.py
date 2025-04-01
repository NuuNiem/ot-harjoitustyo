from entities.user import User
from repositories.user_repository import UserRepository
from repositories.budget_repository import BudgetRepository

class BudgetingService:
    def __init__(self):
        self._user_repository = UserRepository()
        self._budget_repository = BudgetRepository()
        self._current_user = None

    def register_user(self, username, password=""):
        return self._user_repository.create(username, password)

    def get_user(self, username):
        user = self._user_repository.find_by_username(username)
        if not user:
            raise ValueError("User not found")
        self._current_user = username
        return user

    def add_budget_to_user(self, username, budget_name, total_amount):
        return self._budget_repository.create(budget_name, total_amount, username)
    
    def get_user_budgets(self, username):
        return self._budget_repository.find_all_by_username(username)
    
    def add_expense(self, budget_id, description, amount):
        return self._budget_repository.add_expense(budget_id, description, amount)
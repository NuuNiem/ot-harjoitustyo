from .budgeting import Budgeting

class User:
    def __init__(self, username):
        self.username = username
        self.budgets = []

    def create_budget(self, name, total_amount):
        budget = Budgeting(name, total_amount)
        self.budgets.append(budget)
        return budget
    
    def get_budget(self):
        return self.budgets
        
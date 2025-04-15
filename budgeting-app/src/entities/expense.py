class Expense:
    def __init__(self, description, amount, expense_id=None, budget_id=None):
        self.id = expense_id
        self.budget_id = budget_id
        self.description = description
        self.amount = amount

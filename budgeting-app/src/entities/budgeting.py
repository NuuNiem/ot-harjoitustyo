class Budgeting:
    def __init__(self, name, total_amount, budget_id=None):
        self.name = name
        self.total_amount = total_amount
        self.id = budget_id
        self.expenses = []

    def get_remaining_budget(self):
        spent = sum(amount for _, amount in self.expenses)
        return self.total_amount - spent

    def add_expense(self, description, amount):
        self.expenses.append((description, amount))

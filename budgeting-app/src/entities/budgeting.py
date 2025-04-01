class Budgeting:
    def __init__(self, name, total_amount):
        self.name = name
        self.total_amount = total_amount
        self.expenses = []
    
    def add_expense(self, description, amount):
        if self.total_amount < amount:
            raise ValueError("Expense amount exceeds budget")
        self.expenses.append((description, amount)) 
        self.total_amount -= amount
    
    def get_remaining_budget(self):
        return self.total_amount
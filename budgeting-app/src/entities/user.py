from .budgeting import Budgeting


class User:
    """Luokka, joka kuvaa yksittäistä käyttäjää.

    Attributes:
        username: Merkkijonoarvo, joka kuvaa käyttäjän käyttäjätunnusta.
        password: Merkkijonoarvo, joka kuvaa käyttäjän salasanaa.
        budgets: Lista, joka sisältää käyttäjän budjetit.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.budgets = []

    def create_budget(self, name, total_amount):
        budget = Budgeting(name, total_amount)
        self.budgets.append(budget)
        return budget

    def get_budget(self):
        return self.budgets

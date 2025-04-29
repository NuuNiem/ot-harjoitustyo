class Budgeting:
    """Luokka, joka kuvaa yksittäistä budjettia.

    Attributes:
        name: Merkkijonoarvo, joka kuvaa budjetin nimeä.
        total_amount: Kokonaismäärä (float), joka kuvaa budjetin summaa.
        id: Budjetin tunniste (oletuksena None).
        expenses: Lista, joka sisältää budjettiin liittyvät kulut (kuvattuina tupleina).
    """

    def __init__(self, name, total_amount, budget_id=None):
        """Luokan konstruktori, joka luo uuden budjetin.

        Args:
            name: Merkkijonoarvo, joka kuvaa budjetin nimeä.
            total_amount: Kokonaismäärä (float), joka kuvaa budjetin summaa.
            budget_id:
                Vapaaehtoinen, oletusarvoltaan None.
                Budjetin tunniste.
        """
        self.name = name
        self.total_amount = total_amount
        self.id = budget_id
        self.expenses = []

    def get_remaining_budget(self):
        spent = sum(amount for _, amount in self.expenses)
        return self.total_amount - spent

    def add_expense(self, description, amount):
        self.expenses.append((description, amount))

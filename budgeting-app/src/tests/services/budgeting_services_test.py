import unittest
from services.budgeting_services import BudgetingService
from repositories.user_repository import user_repository
from repositories.budget_repository import BudgetRepository


class TestBudgetingService(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()

        self.service = BudgetingService()

        self.service._budget_repository = BudgetRepository()

        self.username1 = "testaaja1"
        self.username2 = "testaaja2"
        self.password = "salasana123"

        self.service.register_user(self.username1, self.password)
        self.service.register_user(self.username2, self.password)

        self.budget_name1 = "Ruoka"
        self.budget_amount1 = 300.0
        self.budget1 = self.service.add_budget_to_user(
            self.username1, self.budget_name1, self.budget_amount1
        )

        self.budget_name2 = "Viihde"
        self.budget_amount2 = 150.0
        self.budget2 = self.service.add_budget_to_user(
            self.username1, self.budget_name2, self.budget_amount2
        )

    def test_register_user(self):
        new_username = "uusikayttaja"
        user = self.service.register_user(new_username, "uusisalasana")
        self.assertEqual(user.username, new_username)

    def test_get_user_found(self):
        user = self.service.get_user(self.username1)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.username1)

    def test_get_user_not_found(self):
        with self.assertRaises(ValueError) as context:
            self.service.get_user("asdasdasd")

    def test_validate_and_create_budget_empty_name(self):
        with self.assertRaises(ValueError) as context:
            self.service.validate_and_create_budget(self.username1, "", "100")

    def test_validate_and_create_budget_zero_amount(self):
        with self.assertRaises(ValueError) as context:
            self.service.validate_and_create_budget(
                self.username1, "Testi", "0")

    def test_validate_and_create_budget_negative_amount(self):
        with self.assertRaises(ValueError) as context:
            self.service.validate_and_create_budget(
                self.username1, "Testi", "-100")

    def test_validate_and_create_budget_invalid_amount_format(self):
        with self.assertRaises(ValueError) as context:
            self.service.validate_and_create_budget(
                self.username1, "Testi", "ei_numero")
        self.assertIn("Invalid amount format", str(context.exception))

    def test_validate_and_create_budget_other_valueerror(self):
        orig_add_budget = self.service.add_budget_to_user

        def raise_other_valueerror(username, name, amount):
            raise ValueError("Virhe")
        self.service.add_budget_to_user = raise_other_valueerror
        with self.assertRaises(ValueError) as context:
            self.service.validate_and_create_budget(
                self.username1, "Testi", "10")
        self.assertIn("Virhe", str(context.exception))
        self.service.add_budget_to_user = orig_add_budget

    def test_add_expense(self):
        expense_desc = "Ruokakauppa"
        expense_amount = 50.0

        expense = self.service.add_expense(
            self.budget1.id, expense_desc, expense_amount
        )

        self.assertIsNotNone(expense)
        self.assertEqual(expense.description, expense_desc)
        self.assertEqual(expense.amount, expense_amount)

        expenses = self.service.get_budget_expenses(self.budget1.id)
        self.assertEqual(len(expenses), 1)

    def test_add_expense_with_string_amount(self):
        expense_desc = "Lätkämatsi"
        expense_amount = "25.50"

        expense = self.service.add_expense(
            self.budget2.id, expense_desc, expense_amount
        )

        self.assertIsNotNone(expense)
        self.assertEqual(expense.description, expense_desc)
        self.assertEqual(expense.amount, float(expense_amount))

        expenses = self.service.get_budget_expenses(self.budget2.id)
        self.assertEqual(len(expenses), 1)

    def test_get_budget_data_for_display(self):
        budgets, budget_map = self.service.get_budget_data_for_display(
            self.username1)

        self.assertGreaterEqual(len(budgets), 2)
        self.assertIn(self.budget_name1, budget_map)
        self.assertIn(self.budget_name2, budget_map)

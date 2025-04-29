import tkinter as tk
from tkinter import ttk, messagebox
from ui.components.budget_tab import BudgetTab
from ui.components.expense_tab import ExpenseTab
from ui.components.budget_summary import BudgetSummary
from ui.components.expense_history import ExpenseHistory
from ui.components.budget_selector import BudgetSelector

class ManageBudgetView:
    """Budjettien hallintanäkymästä vastaava luokka."""

    def __init__(self, root, budgeting_service, username, return_to_menu_callback):
        """Luokan konstruktori.

        Args:
            root: Tkinterin juuri-ikkuna.
            budgeting_service: Budjetointipalvelu, joka hoitaa sovelluslogiikan.
            username: Kirjautuneen käyttäjän käyttäjätunnus.
            return_to_menu_callback: Funktio, jota kutsutaan palattaessa valikkoon.
        """
        self._root = root
        self._budgeting_service = budgeting_service
        self._username = username
        self._return_to_menu_callback = return_to_menu_callback
        self._frame = None
        self._selected_budget_id = None

        self._budget_tab = None
        self._expense_tab = None
        self._budget_selector = None
        self._budget_summary = None
        self._expense_history = None

        self._initialize()

    def _initialize(self):
        """Alustaa budjettien hallintanäkymän."""
        self._create_manage_budget_view()
        self._show_manage_budget_view()
        self._load_data()

    def _create_manage_budget_view(self):
        """Luo budjettien hallintanäkymän komponentit."""
        self._manage_frame = ttk.Frame(self._root, style="Main.TFrame")
        content_frame = ttk.Frame(self._manage_frame, style="Card.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._budget_tab = BudgetTab(left_panel, self._add_budget)
        self._budget_selector = BudgetSelector(left_panel, self._select_budget)
        self._expense_tab = ExpenseTab(left_panel, self._add_expense)
        self._budget_summary = BudgetSummary(right_panel)
        self._expense_history = ExpenseHistory(
            right_panel, self._remove_expense)

        ttk.Button(
            left_panel,
            text="Reset All",
            command=self._reset_all,
            style="Secondary.TButton"
        ).pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            self._manage_frame,
            text="Back to Menu",
            command=self._handle_back_to_menu,
            style="Secondary.TButton"
        ).pack(pady=(20, 0))

    def _add_budget(self, amount, name=None):
        """Lisää uuden budjetin käyttäjälle.

        Args:
            amount: Budjetin kokonaissumma.
            name: (Vapaaehtoinen) Budjetin nimi.

        Returns:
            True, jos budjetin lisäys onnistui, muuten False.
        """
        try:
            if name is None:
                name = f"Budget {amount:.2f}"

            self._budgeting_service.add_budget_to_user(
                self._username, name, amount)
            self._load_data()
            return True
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget amount")
            return False

    def _select_budget(self, budget_id):
        """Valitsee budjetin ja päivittää näkymän.

        Args:
            budget_id: Valitun budjetin tunniste.
        """
        self._selected_budget_id = budget_id
        self._update_selected_budget_view()

    def _update_selected_budget_view(self):
        """Päivittää valitun budjetin tiedot näkymään."""
        if self._selected_budget_id:
            try:
                budget = self._budgeting_service.get_budget_by_id(
                    self._selected_budget_id)
                expenses = self._budgeting_service.get_budget_expenses(
                    self._selected_budget_id)

                total_budget = budget.total_amount
                total_expenses = sum(expense.amount for expense in expenses)
                budget_left = budget.get_remaining_budget()

                self._budget_summary.update(
                    total_budget, total_expenses, budget_left)
                self._expense_history.update(expenses)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Failed to load budget data: {str(e)}")
        else:
            self._budget_summary.update(0, 0, 0)
            self._expense_history.update([])

    def _add_expense(self, title, amount):
        """Lisää uuden kulun valittuun budjettiin.

        Args:
            title: Kulun nimi/kuvaus.
            amount: Kulun määrä.

        Returns:
            True, jos kulun lisäys onnistui, muuten False.
        """
        try:
            if not title:
                messagebox.showerror("Error", "Please enter an expense title")
                return False

            if not self._selected_budget_id:
                messagebox.showerror("Error", "Please select a budget first")
                return False

            self._budgeting_service.add_expense(
                self._selected_budget_id, title, amount)
            self._update_selected_budget_view()
            return True
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid expense amount")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
            return False

    def _remove_expense(self, expense_id):
        """Poistaa kulun budjetista.

        Args:
            expense_id: Kulun tunniste.
        """
        self._budgeting_service.remove_expense(expense_id)
        self._update_selected_budget_view()

    def _reset_all(self):
        """Nollaa kaikki käyttäjän budjetit ja kulut."""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all budgets and expenses?"):
            budgets = self._budgeting_service.get_user_budgets(self._username)
            for budget in budgets:
                expenses = self._budgeting_service.get_budget_expenses(
                    budget.id)
                for expense in expenses:
                    self._budgeting_service.remove_expense(expense.id)
                self._budgeting_service.remove_budget(budget.id)
            self._selected_budget_id = None
            self._load_data()

    def _load_data(self):
        """Lataa käyttäjän budjetit ja päivittää näkymän."""
        try:
            budgets = self._budgeting_service.get_user_budgets(self._username)
            self._budget_selector.update_budgets(budgets)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def _handle_back_to_menu(self):
        """Palaa päävalikkoon."""
        self.destroy()
        self._return_to_menu_callback()

    def _show_manage_budget_view(self):
        """Näyttää budjettien hallintanäkymän."""
        if self._frame:
            self._frame.place_forget()

        self._manage_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._frame = self._manage_frame

    def destroy(self):
        """Tuhoaa näkymän ja sen komponentit."""
        if self._budget_tab:
            self._budget_tab.destroy()

        if self._budget_selector:
            self._budget_selector.destroy()

        if self._expense_tab:
            self._expense_tab.destroy()

        if self._budget_summary:
            self._budget_summary.destroy()

        if self._expense_history:
            self._expense_history.destroy()

        if self._frame:
            self._frame.place_forget()
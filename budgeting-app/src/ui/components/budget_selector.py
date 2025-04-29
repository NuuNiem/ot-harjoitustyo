import tkinter as tk
from tkinter import ttk


class BudgetSelector:
    def __init__(self, parent, select_budget_callback):
        self._parent = parent
        self._select_budget_callback = select_budget_callback
        self._frame = ttk.Frame(parent, padding=(0, 0, 0, 10))
        self._budgets = []
        self._selected_budget_id = None
        self._initialize()

    def _initialize(self):
        self._frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            self._frame,
            text="Select Budget:",
            style="SubHeader.TLabel"
        ).pack(anchor=tk.W, pady=(0, 5))

        self._budget_var = tk.StringVar()
        self._budget_dropdown = ttk.Combobox(
            self._frame,
            textvariable=self._budget_var,
            state="readonly",
            style="Standard.TCombobox"
        )
        self._budget_dropdown.pack(fill=tk.X)

        self._budget_dropdown.bind(
            "<<ComboboxSelected>>", self._on_budget_selected)

    def _on_budget_selected(self, event):
        selected_name = self._budget_var.get()

        # Find the budget ID for the selected name
        for budget in self._budgets:
            if f"{budget.name} (${budget.total_amount:.2f})" == selected_name:
                self._selected_budget_id = budget.id
                self._select_budget_callback(budget.id)
                break

    def update_budgets(self, budgets):
        self._budgets = budgets

        budget_names = [
            f"{budget.name} (${budget.total_amount:.2f})" for budget in budgets]

        self._budget_dropdown['values'] = budget_names

        if budget_names and (self._selected_budget_id is None or
                             not any(b.id == self._selected_budget_id for b in budgets)):
            self._budget_dropdown.current(0)
            self._selected_budget_id = budgets[0].id if budgets else None
            self._select_budget_callback(self._selected_budget_id)
        elif not budget_names:
            self._budget_var.set("")
            self._selected_budget_id = None
        else:
            for i, budget in enumerate(budgets):
                if budget.id == self._selected_budget_id:
                    self._budget_dropdown.current(i)
                    break

    def get_selected_budget_id(self):
        return self._selected_budget_id

    def get_frame(self):
        return self._frame

    def destroy(self):
        self._frame.destroy()

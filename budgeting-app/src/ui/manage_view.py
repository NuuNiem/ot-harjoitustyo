import tkinter as tk
from tkinter import ttk
from ui.budget_tab import CreateBudgetTab
from ui.expense_tab import AddExpenseTab


class ManageBudgetView:
    def __init__(self, root, budgeting_service, username, return_to_menu_callback):
        self._root = root
        self._budgeting_service = budgeting_service
        self._username = username
        self._return_to_menu_callback = return_to_menu_callback
        self._frame = None

        self._initialize()

    def _initialize(self):
        self._create_manage_view()
        self._show_manage_view()

    def _create_manage_view(self):
        self._manage_frame = ttk.Frame(self._root, padding=20)

        self._notebook = ttk.Notebook(self._manage_frame)
        self._notebook.grid(row=0, column=0, pady=10, sticky="nsew")

        self._create_budget_tab = CreateBudgetTab(
            self._notebook,
            self._budgeting_service,
            self._username,
            self._refresh_tabs
        )
        self._notebook.add(self._create_budget_tab.frame, text="Create Budget")

        self._add_expense_tab = AddExpenseTab(
            self._notebook,
            self._budgeting_service,
            self._username,
            self._refresh_tabs
        )
        self._notebook.add(self._add_expense_tab.frame, text="Add Expense")

        ttk.Button(
            self._manage_frame,
            text="Back to Menu",
            command=self._handle_back_to_menu
        ).grid(row=1, column=0, pady=(20, 0))

    def _refresh_tabs(self):
        self._create_budget_tab.refresh()
        self._add_expense_tab.refresh()

    def _handle_back_to_menu(self):
        self.destroy()
        self._return_to_menu_callback()

    def _show_manage_view(self):
        if self._frame:
            self._frame.place_forget()

        self._manage_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._frame = self._manage_frame

    def destroy(self):
        if self._frame:
            self._frame.place_forget()

import tkinter as tk
from tkinter import ttk
from ui.login_view import LoginView
from ui.menu import Menu
from ui.manage_view import ManageBudgetView
import sv_ttk


class BudgetingUI:
    def __init__(self, root, budgeting_service):
        self._root = root
        self._budgeting_service = budgeting_service
        self._current_view = None
        self._current_user = None

        sv_ttk.set_theme("dark")

        self._initialize_styles()

    def _initialize_styles(self):
        self._style = ttk.Style()

        self._style.configure("Link.TLabel",
                              cursor="hand2",
                              font=("Ubuntu", 11))

        self._style.configure("Header.TLabel",
                              font=("Ubuntu", 16, "bold"))

        self._style.configure("SubHeader.TLabel",
                              font=("Ubuntu", 14, "bold"))

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._budgeting_service,
            self._handle_successful_login
        )

    def _handle_successful_login(self, username):
        self._current_user = username
        self._show_main_menu()

    def _show_main_menu(self):
        self._hide_current_view()
        self._current_view = Menu(
            self._root,
            self._budgeting_service,
            self._current_user,
            self._show_login_view,
            self._show_manage_budgets_view
        )

    def _show_manage_budgets_view(self):
        self._hide_current_view()
        self._current_view = ManageBudgetView(
            self._root,
            self._budgeting_service,
            self._current_user,
            self._show_main_menu
        )

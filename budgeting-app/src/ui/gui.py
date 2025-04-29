import tkinter as tk
from tkinter import ttk
from ui.login_view import LoginView
from ui.menu import Menu
from ui.manage_view import ManageBudgetView
import sv_ttk


class BudgetingUI:
    """Sovelluksen graafisesta käyttöliittymästä vastaava luokka."""

    def __init__(self, root, budgeting_service):
        """Luokan konstruktori.

        Args:
            root: Tkinterin juuri-ikkuna.
            budgeting_service: Budjetointipalvelu, joka hoitaa sovelluslogiikan.
        """
        self._root = root
        self._budgeting_service = budgeting_service
        self._current_view = None
        self._current_user = None

        sv_ttk.set_theme("dark")

        self._initialize_styles()

    def _initialize_styles(self):
        """Alustaa käyttöliittymän tyylit."""
        self._style = ttk.Style()

        self._style.configure("Link.TLabel",
                              cursor="hand2",
                              font=("Liberation Sans", 11))

        self._style.configure("Header.TLabel",
                              font=("Liberation Sans", 16, "bold"))

        self._style.configure("SubHeader.TLabel",
                              font=("Liberation Sans", 14, "bold"))

    def start(self):
        """Käynnistää käyttöliittymän näyttämällä kirjautumisnäkymän."""
        self._show_login_view()

    def _hide_current_view(self):
        """Piilottaa nykyisen näkymän."""
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_login_view(self):
        """Näyttää kirjautumisnäkymän."""
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._budgeting_service,
            self._handle_successful_login
        )

    def _handle_successful_login(self, username):
        """Käsittelee onnistuneen kirjautumisen.

        Args:
            username: Kirjautuneen käyttäjän käyttäjätunnus.
        """
        self._current_user = username
        self._show_main_menu()

    def _show_main_menu(self):
        """Näyttää päävalikon."""
        self._hide_current_view()
        self._current_view = Menu(
            self._root,
            self._budgeting_service,
            self._current_user,
            self._show_login_view,
            self._show_manage_budgets_view
        )

    def _show_manage_budgets_view(self):
        """Näyttää budjettien hallintanäkymän."""
        self._hide_current_view()
        self._current_view = ManageBudgetView(
            self._root,
            self._budgeting_service,
            self._current_user,
            self._show_main_menu
        )
import tkinter as tk
from tkinter import ttk, messagebox


class Menu:
    def __init__(self, main_frame, budgeting_service, username, logout_callback,
                 manage_budgets_callback):
        self._main_frame = main_frame
        self._budgeting_service = budgeting_service
        self._username = username
        self._logout_callback = logout_callback
        self._manage_budgets_callback = manage_budgets_callback
        self._menu_frame = None

        self._initialize()

    def _initialize(self):
        for widget in self._main_frame.winfo_children():
            widget.destroy()

        self._menu_frame = ttk.Frame(self._main_frame)

        if self._username:
            welcome_label = ttk.Label(
                self._menu_frame,
                text=f"Welcome, {self._username}!",
                style="SubHeader.TLabel",
            )

            welcome_label.grid(row=0, column=0, pady=(0, 30))

        manage_budgets_btn = ttk.Button(
            self._menu_frame,
            text="Manage Budgets",
            command=self._manage_budgets_callback,
            width=15
        )

        visualise_budgets_btn = ttk.Button(
            self._menu_frame,
            text="Visualise Budgets",
            width=15
        )

        visualise_budgets_btn.grid(row=1, column=0, pady=(5))
        manage_budgets_btn.grid(row=2, column=0, pady=5)

        logout_btn = ttk.Button(
            self._menu_frame,
            text="Log out",
            command=self._handle_logout,
            style="Secondary.TButton"
        )
        logout_btn.grid(row=3, column=0, pady=(20, 0))

        self._menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _handle_logout(self):
        if messagebox.askyesno("Log out", "Are you sure you want to log out?"):
            self._logout_callback()

    def destroy(self):
        if self._menu_frame:
            self._menu_frame.place_forget()

import tkinter as tk
from tkinter import ttk, messagebox


class RegisterView:
    def __init__(self, root, budgeting_service, return_to_login_callback):
        self._root = root
        self._budgeting_service = budgeting_service
        self._return_to_login_callback = return_to_login_callback
        self._frame = None

        self._initialize()

    def _initialize(self):
        self._create_register_view()
        self._show_register_view()

    def _create_register_view(self):
        self._register_frame = ttk.Frame(self._root, style="Main.TFrame")

        ttk.Label(self._register_frame, text="Create a New Account",
                  style="Header.TLabel").grid(row=0, column=0, pady=20)

        self._reg_username_entry = ttk.Entry(self._register_frame, width=30,
                                             style="Standard.TEntry")
        self._reg_username_entry.grid(row=1, column=0, pady=10)
        self._reg_username_entry.insert(0, "Username")

        self._reg_password_entry = ttk.Entry(self._register_frame, width=30,
                                             style="Standard.TEntry")
        self._reg_password_entry.grid(row=2, column=0, pady=10)
        self._reg_password_entry.insert(0, "Password")

        self._reg_username_entry.bind(
            "<FocusIn>", lambda e: self._on_entry_focus_in(e, "Username"))
        self._reg_username_entry.bind(
            "<FocusOut>", lambda e: self._on_entry_focus_out(e, "Username"))

        self._reg_password_entry.bind(
            "<FocusIn>", lambda e: self._on_entry_focus_in(e, "Password", show="*"))
        self._reg_password_entry.bind(
            "<FocusOut>", lambda e: self._on_entry_focus_out(e, "Password", show="*"))

        button_frame = ttk.Frame(self._register_frame)
        button_frame.grid(row=3, column=0, pady=20)

        ttk.Button(button_frame, text="Back", style="Secondary.TButton",
                   command=self._handle_back_to_login).grid(row=0, column=0, padx=5)

        ttk.Button(button_frame, text="Register", style="Primary.TButton",
                   command=self._handle_register).grid(row=0, column=1, padx=5)

    def _on_entry_focus_in(self, event, placeholder, show=None):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            if show:
                event.widget.config(show=show)

    def _on_entry_focus_out(self, event, placeholder, show=None):
        if event.widget.get() == "":
            if show:
                event.widget.config(show="")
            event.widget.insert(0, placeholder)

    def _show_register_view(self):
        if self._frame:
            self._frame.place_forget()

        self._register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._frame = self._register_frame

    def _handle_register(self):
        username = self._reg_username_entry.get()
        password = self._reg_password_entry.get()

        if username == "Username" or password == "Password" or len(username) == 0 or len(password) == 0:
            messagebox.showerror("Registration Error",
                                 "Username and password is required")
            return
        try:
            self._budgeting_service.register_user(username, password)
            messagebox.showinfo("Registration Successful",
                                "Your account has been created.")
            self._handle_back_to_login()
        except ValueError as e:
            messagebox.showerror("Registration Error", str(e))

    def _handle_back_to_login(self):
        self.destroy()
        self._return_to_login_callback()

    def destroy(self):
        if self._frame:
            self._frame.place_forget()

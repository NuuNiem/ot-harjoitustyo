import tkinter as tk
from tkinter import ttk, messagebox


class LoginView:
    def __init__(self, root, budgeting_service, handle_login):
        self._root = root
        self._budgeting_service = budgeting_service
        self._handle_login = handle_login
        self._frame = None
        self._username_entry = None
        self._password_entry = None

        self._initialize()

    def _initialize(self):
        self._frame = ttk.Frame(self._root, style="Main.TFrame")

        ttk.Label(self._frame, text="Login",
                  style="Header.TLabel").grid(row=0, column=0, pady=20)

        self._initialize_username_field()
        self._initialize_password_field()
        self._initialize_buttons()

        self._frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def _initialize_username_field(self):
        self._username_entry = ttk.Entry(
            self._frame, width=30, style="Standard.TEntry")
        self._username_entry.grid(row=1, column=0, pady=10)
        self._username_entry.insert(0, "Username")

        self._username_entry.bind(
            "<FocusIn>", lambda e: self._entry_focus_in(e, "Username"))
        self._username_entry.bind(
            "<FocusOut>", lambda e: self._entry_focus_out(e, "Username"))

    def _initialize_password_field(self):
        self._password_entry = ttk.Entry(
            self._frame, width=30, style="Standard.TEntry")
        self._password_entry.grid(row=2, column=0, pady=10)
        self._password_entry.insert(0, "Password")

        self._password_entry.bind(
            "<FocusIn>", lambda e: self._entry_focus_in(e, "Password", show="*"))
        self._password_entry.bind(
            "<FocusOut>", lambda e: self._entry_focus_out(e, "Password", show="*"))

    def _initialize_buttons(self):
        ttk.Button(
            self._frame,
            text="Login",
            style="Primary.TButton",
            command=self._login_handler
        ).grid(row=3, column=0, pady=20)

        register_label = ttk.Label(
            self._frame,
            text="No account yet? Click here",
            style="Link.TLabel"
        )
        register_label.grid(row=4, column=0, pady=10)
        register_label.bind("<Button-1>", lambda e: self._show_register_view())

    def _entry_focus_in(self, event, placeholder, show=None):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            if show:
                event.widget.config(show=show)

    def _entry_focus_out(self, event, placeholder, show=None):
        if event.widget.get() == "":
            if show:
                event.widget.config(show="")
            event.widget.insert(0, placeholder)

    def _login_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if username == "Username":
            username = ""
        if password == "Password":
            password = ""

        try:
            user = self._budgeting_service.get_user(username)
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")

            self.destroy()
            self._handle_login(username)

        except ValueError as e:
            messagebox.showerror(
                "Login Error", "User not found. Please register first.")

    def _show_register_view(self):
        from ui.register_view import RegisterView
        self.destroy()
        RegisterView(
            self._root,
            self._budgeting_service,
            self._show_login_after_register
        )

    def _show_login_after_register(self):
        self._initialize()

    def destroy(self):
        if self._frame:
            self._frame.place_forget()

import tkinter as tk
from tkinter import ttk, messagebox
from ui.register_view import RegisterView

class LoginView:
    def __init__(self, root, budgeting_service, login_callback):
        self._root = root
        self._budgeting_service = budgeting_service
        self._login_callback = login_callback
        self._frame = None
        
        self._initialize()
    
    def _initialize(self):
        self._create_login_view()
        self._show_login_view()
    
    def _create_login_view(self):
        self._login_frame = ttk.Frame(self._root, padding=20)
        
        ttk.Label(self._login_frame, text="Login", 
                  style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(self._login_frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self._username_entry = ttk.Entry(self._login_frame, width=30)
        self._username_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(self._login_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self._password_entry = ttk.Entry(self._login_frame, width=30, show="*")
        self._password_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Button(self._login_frame, text="Login", 
                  command=self._handle_login).grid(row=3, column=0, columnspan=2, pady=20)
        
        no_account_label = ttk.Label(self._login_frame, text="No account yet? Click here", 
                                     foreground="blue", cursor="hand2")
        no_account_label.grid(row=4, column=0, columnspan=2, pady=10)
        no_account_label.bind("<Button-1>", lambda e: self._handle_show_register())
    
    def _show_login_view(self):        
        if self._frame:
            self._frame.place_forget()
            
        self._login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._frame = self._login_frame
    
    def _handle_login(self):
        username = self._username_entry.get()
        password = self._password_entry.get() 
        
        try:
            user = self._budgeting_service.get_user(username)
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self._login_callback(username)
        except ValueError as e:
            messagebox.showerror("Login Error", "User not found. Please register first.")
    
    def _handle_show_register(self):
        from ui.register_view import RegisterView
        self.destroy()
        register_view = RegisterView(
            self._root,
            self._budgeting_service,
            self._show_login_after_register
        )
    
    def _show_login_after_register(self):
        self._initialize()
        
    def destroy(self):
        if self._frame:
            self._frame.place_forget()
import tkinter as tk
from tkinter import ttk
from ui.login_view import LoginView

class BudgetingUI:
    def __init__(self, root, budgeting_service):
        self._root = root
        self._budgeting_service = budgeting_service
        self._current_view = None
        self._current_user = None
        self._initialize_styles()
    
    def _initialize_styles(self):
        self._style = ttk.Style()
        self._available_themes = self._style.theme_names()
        # Default themes include: 'alt', 'clam', 'classic', 'default', 'vista'
        
        # Set a theme (e.g., 'clam' is often darker)
        self._style.theme_use('alt')  # You can change this to any available theme
        
        # Additional style configurations
        self._style.configure("Header.TLabel", font=("Arial", 16, "bold"))
    
    def start(self):
        self._show_login_view()
    
    def _show_login_view(self):
        if self._current_view:
            self._current_view.destroy()
        
        self._current_view = LoginView(
            self._root, 
            self._budgeting_service,
            self._handle_successful_login
        )
    
    def _handle_successful_login(self, username):
        self._current_user = username
        self._show_budget_view()
    
    def _show_budget_view(self):
        if self._current_view:
            self._current_view.destroy()
            
        frame = ttk.Frame(self._root, padding=20)
        ttk.Label(
            frame, 
            text=f"Welcome, {self._current_user}!\nYou are now logged in.",
            font=("Arial", 14)
        ).pack(pady=20)
        
        ttk.Button(
            frame, 
            text="Logout",
            command=self._show_login_view
        ).pack(pady=10)
        
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._current_view = type('SimpleView', (), {
            'destroy': lambda: frame.place_forget()
        })()
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
        self._register_frame = ttk.Frame(self._root, padding=20)
        
        ttk.Label(self._register_frame, text="Create a New Account", 
                  style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(self._register_frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self._reg_username_entry = ttk.Entry(self._register_frame, width=30)
        self._reg_username_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(self._register_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self._reg_password_entry = ttk.Entry(self._register_frame, width=30, show="*")
        self._reg_password_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Button(self._register_frame, text="Register", 
                  command=self._handle_register).grid(row=3, column=1, pady=20)
        
        ttk.Button(self._register_frame, text="Back", 
                  command=self._handle_back_to_login).grid(row=3, column=0, pady=20)
    
    def _show_register_view(self):
        if self._frame:
            self._frame.place_forget()
            
        self._register_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self._frame = self._register_frame
    
    def _handle_register(self):
        username = self._reg_username_entry.get()
        password = self._reg_password_entry.get() 
        
        if not username:
            messagebox.showerror("Registration Error", "Username cannot be empty.")
            return
        
        try:
            self._budgeting_service.register_user(username)
            messagebox.showinfo("Registration Successful", "Your account has been created.")
            self._handle_back_to_login()
        except ValueError as e:
            messagebox.showerror("Registration Error", str(e))
    
    def _handle_back_to_login(self):
        self.destroy()
        self._return_to_login_callback()
    
    def destroy(self):
        if self._frame:
            self._frame.place_forget()
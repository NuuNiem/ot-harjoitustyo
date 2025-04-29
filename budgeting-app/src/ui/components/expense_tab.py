import tkinter as tk
from tkinter import ttk, messagebox


class ExpenseTab:
    def __init__(self, parent, add_expense_callback):
        self._parent = parent
        self._add_expense_callback = add_expense_callback
        self._frame = ttk.Frame(parent, padding=10)
        self._initialize()

    def _initialize(self):
        self._frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            self._frame,
            text="Add Expense",
            style="SubHeader.TLabel"
        ).pack(anchor=tk.W)

        ttk.Label(self._frame, text="Expense Title:",
                  style="Body.TLabel").pack(anchor=tk.W, pady=(10, 2))

        self._expense_title_entry = ttk.Entry(
            self._frame, style="Standard.TEntry")
        self._expense_title_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self._frame, text="Amount:", style="Body.TLabel").pack(
            anchor=tk.W, pady=(0, 2))

        self._expense_amount_entry = ttk.Entry(
            self._frame, style="Standard.TEntry")
        self._expense_amount_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            self._frame,
            text="Add Expense",
            command=self._handle_add_expense,
            style="Secondary.TButton"
        ).pack(fill=tk.X)

    def _handle_add_expense(self):
        title = self._expense_title_entry.get()
        amount_text = self._expense_amount_entry.get()

        try:
            amount = float(amount_text)
            success = self._add_expense_callback(title, amount)
            if success:
                self._expense_title_entry.delete(0, tk.END)
                self._expense_amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid expense amount")

    def get_frame(self):
        return self._frame

    def destroy(self):
        self._frame.destroy()

import tkinter as tk
from tkinter import ttk, messagebox


class BudgetTab:
    def __init__(self, parent, add_budget_callback):
        self._parent = parent
        self._add_budget_callback = add_budget_callback
        self._frame = ttk.Frame(parent, padding=10)
        self._initialize()

    def _initialize(self):
        self._frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            self._frame,
            text="Add Budget",
            style="SubHeader.TLabel"
        ).pack(anchor=tk.W)

        ttk.Label(self._frame, text="Budget Name:", style="Body.TLabel").pack(
            anchor=tk.W, pady=(10, 2))

        self._budget_name_entry = ttk.Entry(
            self._frame, style="Standard.TEntry")
        self._budget_name_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(self._frame, text="Budget Amount:", style="Body.TLabel").pack(
            anchor=tk.W, pady=(0, 2))

        self._budget_entry = ttk.Entry(self._frame, style="Standard.TEntry")
        self._budget_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            self._frame,
            text="Add Budget",
            command=self._handle_add_budget,
            style="Secondary.TButton"
        ).pack(fill=tk.X)

    def _handle_add_budget(self):
        try:
            name = self._budget_name_entry.get().strip()
            amount_text = self._budget_entry.get().strip()

            if not amount_text:
                messagebox.showerror("Error", "Please enter a budget amount")
                return

            amount = float(amount_text)

            if not name:
                name = f"Budget {amount:.2f}"

            success = self._add_budget_callback(amount, name)
            if success:
                self._budget_name_entry.delete(0, tk.END)
                self._budget_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget amount")

    def get_frame(self):
        return self._frame

    def destroy(self):
        self._frame.destroy()

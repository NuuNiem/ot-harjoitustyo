import tkinter as tk
from tkinter import ttk


class BudgetSummary:
    def __init__(self, parent):
        self._parent = parent
        self._frame = ttk.Frame(parent)
        self._initialize()

    def _initialize(self):
        self._frame.pack(fill=tk.X, pady=(0, 20))

        self._total_budget_label = ttk.Label(
            self._frame,
            text="Total Budget: 0.00",
            style="Body.TLabel",
            padding=10
        )
        self._total_budget_label.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self._total_expenses_label = ttk.Label(
            self._frame,
            text="Total Expenses: 0.00",
            style="Body.TLabel",
            padding=10
        )
        self._total_expenses_label.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self._budget_left_label = ttk.Label(
            self._frame,
            text="Budget Left: 0.00",
            style="Body.TLabel",
            padding=10
        )
        self._budget_left_label.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def update(self, total_budget, total_expenses, budget_left):
        self._total_budget_label.config(
            text=f"Total Budget: {total_budget:.2f}")
        self._total_expenses_label.config(
            text=f"Total Expenses: {total_expenses:.2f}")
        self._budget_left_label.config(text=f"Budget Left: {budget_left:.2f}")

    def get_frame(self):
        return self._frame

    def destroy(self):
        self._frame.destroy()

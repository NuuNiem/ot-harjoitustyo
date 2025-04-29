import tkinter as tk
from tkinter import ttk


class ExpenseHistory:
    def __init__(self, parent, remove_expense_callback):
        self._parent = parent
        self._remove_expense_callback = remove_expense_callback
        self._frame = ttk.Frame(parent)
        self._expense_items = []
        self._initialize()

    def _initialize(self):
        self._frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self._frame,
            text="Expense History:",
            style="SubHeader.TLabel"
        ).pack(anchor=tk.W, pady=(0, 10))

        headers_frame = ttk.Frame(self._frame)
        headers_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(
            headers_frame,
            text="Expense Name",
            width=25,
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Label(
            headers_frame,
            text="Amount",
            width=15,
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Label(
            headers_frame,
            text="Action",
            width=10,
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Separator(self._frame, orient=tk.HORIZONTAL).pack(
            fill=tk.X, pady=5)

        self._expense_canvas = tk.Canvas(self._frame)
        scrollbar = ttk.Scrollbar(
            self._frame, orient=tk.VERTICAL, command=self._expense_canvas.yview)

        self._expense_list_frame = ttk.Frame(self._expense_canvas)
        self._expense_list_frame.bind(
            "<Configure>",
            lambda e: self._expense_canvas.configure(
                scrollregion=self._expense_canvas.bbox("all"))
        )

        self._expense_canvas.create_window(
            (0, 0), window=self._expense_list_frame, anchor=tk.NW)
        self._expense_canvas.configure(yscrollcommand=scrollbar.set)

        self._expense_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update(self, expenses):
        for widget in self._expense_list_frame.winfo_children():
            widget.destroy()

        self._expense_items = []

        if expenses:
            for expense in expenses:
                self._add_expense_item(expense)
        else:
            ttk.Label(
                self._expense_list_frame,
                text="No expenses found. Add some expenses!",
                style="Body.TLabel",
                padding=10
            ).pack(fill=tk.X)

    def _add_expense_item(self, expense):
        item_frame = ttk.Frame(self._expense_list_frame)
        item_frame.pack(fill=tk.X, pady=2)

        ttk.Label(
            item_frame,
            text=expense.description,
            width=25,
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=(5, 0))

        ttk.Label(
            item_frame,
            text=f"{expense.amount:.2f}",
            width=15,
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(
            item_frame,
            text="Remove",
            command=lambda e=expense: self._remove_expense_callback(e.id),
            style="Secondary.TButton",
            width=10
        ).pack(side=tk.LEFT, padx=(10, 0))

        self._expense_items.append(item_frame)

    def get_frame(self):
        return self._frame

    def destroy(self):
        self._frame.destroy()

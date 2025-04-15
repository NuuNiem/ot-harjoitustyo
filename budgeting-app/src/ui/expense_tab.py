import tkinter as tk
from tkinter import ttk, messagebox


class AddExpenseTab:
    def __init__(self, parent, budgeting_service, username, refresh_callback=None):
        self.frame = ttk.Frame(parent, padding=10)
        self._budgeting_service = budgeting_service
        self._username = username
        self._refresh_callback = refresh_callback
        self._selected_budget = None

        self._initialize()

    def _initialize(self):
        ttk.Label(
            self.frame,
            text="Add Expense to Budget",
            style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(
            self.frame,
            text="Select Budget:"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self._selected_budget_var = tk.StringVar()
        self._budget_dropdown = ttk.Combobox(
            self.frame,
            textvariable=self._selected_budget_var,
            state="readonly",
            width=28
        )
        self._budget_dropdown.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(
            self.frame,
            text="Expense Description:"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self._expense_description = ttk.Entry(self.frame, width=30)
        self._expense_description.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Label(
            self.frame,
            text="Expense Amount:"
        ).grid(row=3, column=0, sticky="w", pady=5)

        self._expense_amount = ttk.Entry(self.frame, width=30)
        self._expense_amount.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Button(
            self.frame,
            text="Add Expense",
            command=self._handle_add_expense
        ).grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Label(
            self.frame,
            text="Current Expenses:",
            font=("", 12, "bold")
        ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 10))

        self._expenses_list_frame = ttk.Frame(self.frame)
        self._expenses_list_frame.grid(
            row=6, column=0, columnspan=2, sticky="nsew")

        self._expenses_scrollbar = ttk.Scrollbar(self._expenses_list_frame)
        self._expenses_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._expenses_listbox = tk.Listbox(
            self._expenses_list_frame,
            width=50,
            height=8,
            yscrollcommand=self._expenses_scrollbar.set
        )
        self._expenses_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._expenses_scrollbar.config(command=self._expenses_listbox.yview)

        self._budget_dropdown.bind(
            "<<ComboboxSelected>>", self._update_expenses_list)

        self._load_budget_dropdown()

    def _load_budget_dropdown(self):
        try:
            budgets, self._budget_map = self._budgeting_service.get_budget_data_for_display(
                self._username)

            self._budget_dropdown['values'] = []
            self._selected_budget_var.set("")

            if budgets:
                self._budget_dropdown['values'] = list(self._budget_map.keys())

                if budgets:
                    self._budget_dropdown.current(0)
                    self._update_expenses_list(None)
            else:
                self._expenses_listbox.delete(0, tk.END)
                self._expenses_listbox.insert(
                    tk.END, "No budgets found. Create a budget first!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load budgets: {str(e)}")

    def _update_expenses_list(self, event):
        selected_budget_name = self._selected_budget_var.get()

        if not selected_budget_name or selected_budget_name not in self._budget_map:
            return

        self._selected_budget = self._budget_map[selected_budget_name]
        self._expenses_listbox.delete(0, tk.END)

        try:
            expenses = self._budgeting_service.get_budget_expenses(
                self._selected_budget.id)

            if not expenses:
                self._expenses_listbox.insert(
                    tk.END, "No expenses for this budget yet.")
            else:
                for expense in expenses:
                    self._expenses_listbox.insert(
                        tk.END,
                        f"{expense.description} - ${expense.amount:.2f}"
                    )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {str(e)}")

    def _handle_add_expense(self):
        if not self._selected_budget:
            messagebox.showerror("Error", "Please select a budget first")
            return

        description = self._expense_description.get().strip()
        amount_str = self._expense_amount.get().strip()

        try:
            self._budgeting_service.validate_and_add_expense(
                self._selected_budget.id,
                description,
                amount_str
            )

            messagebox.showinfo(
                "Success", f"Expense added to '{self._selected_budget.name}' successfully!")

            self._expense_description.delete(0, tk.END)
            self._expense_amount.delete(0, tk.END)
            self._update_expenses_list(None)

            if self._refresh_callback:
                self._refresh_callback()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

    def refresh(self):
        self._load_budget_dropdown()

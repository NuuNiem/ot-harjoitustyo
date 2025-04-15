import tkinter as tk
from tkinter import ttk, messagebox


class CreateBudgetTab:
    def __init__(self, parent, budgeting_service, username, refresh_callback=None):
        self.frame = ttk.Frame(parent, padding=10)
        self._budgeting_service = budgeting_service
        self._username = username
        self._refresh_callback = refresh_callback

        self._initialize()

    def _initialize(self):
        ttk.Label(
            self.frame,
            text="Create New Budget",
            style="Header.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(
            self.frame,
            text="Budget Name:"
        ).grid(row=1, column=0, sticky="w", pady=5)

        self._budget_name = ttk.Entry(self.frame, width=30)
        self._budget_name.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(
            self.frame,
            text="Total Amount:"
        ).grid(row=2, column=0, sticky="w", pady=5)

        self._budget_amount = ttk.Entry(self.frame, width=30)
        self._budget_amount.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Button(
            self.frame,
            text="Create Budget",
            command=self._handle_create_budget
        ).grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Label(
            self.frame,
            text="Your Existing Budgets:",
            font=("", 12, "bold")
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(20, 10))

        self._budget_list_frame = ttk.Frame(self.frame)
        self._budget_list_frame.grid(
            row=5, column=0, columnspan=2, sticky="nsew")

        self._budget_scrollbar = ttk.Scrollbar(self._budget_list_frame)
        self._budget_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._budget_listbox = tk.Listbox(
            self._budget_list_frame,
            width=50,
            height=8,
            yscrollcommand=self._budget_scrollbar.set
        )
        self._budget_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._budget_scrollbar.config(command=self._budget_listbox.yview)

        self._load_budgets()

    def _load_budgets(self):
        self._budget_listbox.delete(0, tk.END)

        try:
            budgets = self._budgeting_service.get_user_budgets(self._username)

            if not budgets:
                self._budget_listbox.insert(
                    tk.END, "No budgets found. Create your first budget!")
            else:
                for budget in budgets:
                    self._budget_listbox.insert(
                        tk.END,
                        f"{budget.name} - Total: {budget.total_amount:.2f}€ - Remaining: {budget.get_remaining_budget():.2f}€"
                    )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load budgets: {str(e)}")

    def _handle_create_budget(self):
        name = self._budget_name.get().strip()
        amount_str = self._budget_amount.get().strip()

        try:
            self._budgeting_service.validate_and_create_budget(
                self._username,
                name,
                amount_str
            )

            messagebox.showinfo(
                "Success", f"Budget '{name}' created successfully!")

            self._budget_name.delete(0, tk.END)
            self._budget_amount.delete(0, tk.END)
            self._load_budgets()

            if self._refresh_callback:
                self._refresh_callback()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create budget: {str(e)}")

    def refresh(self):
        self._load_budgets()

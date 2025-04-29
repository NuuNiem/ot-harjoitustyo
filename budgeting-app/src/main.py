import tkinter as tk
import os
from services.budgeting_services import BudgetingService
from ui.gui import BudgetingUI
from initialize_database import initialize_database


def main():
    dirname = os.path.dirname(__file__)
    data_dir = os.path.join(dirname, "..", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    initialize_database()
    root = tk.Tk()
    root.title("Budgeting App")
    root.geometry("900x700")

    root.minsize(800, 600)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 700) // 2
    root.geometry(f"900x700+{x}+{y}")

    budgeting_service = BudgetingService()
    budgeting_ui = BudgetingUI(root, budgeting_service)
    budgeting_ui.start()

    root.mainloop()


if __name__ == "__main__":
    main()

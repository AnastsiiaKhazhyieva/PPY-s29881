import tkinter as tk
from game_window import GameWindow
from db_engine import session
from model_db import Category
from settings_window import WindowManager
from global_settings import get_button_style

class CategoryWindow:
    def __init__(self, parent, game_mode, menu):
        self.parent = parent
        self.game_mode = game_mode
        self.menu = menu
        self.parent.title("Wybór kategorii")
        self.parent.protocol("WM_DELETE_WINDOW", self.menu.return_to_menu)
        WindowManager.center_window(parent, 430, 250)

        label = tk.Label(parent, text="Wybierz kategorię:", font=("Arial", 16))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        self.categories = [c.name for c in session.query(Category).order_by(Category.name).all()]

        for index, name in enumerate(self.categories):
            row = index % 3 + 1
            col = index // 3
            button = tk.Button(parent, text=name, width=20, height=2,
                               command=lambda n=name: self.select_category(n), **get_button_style())
            button.grid(row=row, column=col, padx=10, pady=5)

    def select_category(self, category_name):
        self.parent.destroy()
        game_window = tk.Toplevel()
        GameWindow(game_window, category_name, self.game_mode, on_exit=self.menu.return_to_menu)

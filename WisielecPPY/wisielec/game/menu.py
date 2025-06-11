import tkinter as tk
from tkinter import messagebox
from login_window import LoginWindow
from settings_window import open_settings_window
from start_config_window import open_start_config_window
from scoreboard_window import open_scoreboard_window
from authorization import load_session, clear_session
from model_db import User
from db_engine import session
from global_settings import WindowManager
from global_settings import settings
from player_input_window import open_player_input_window
from global_settings import get_button_style

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu")
        WindowManager.center_window(self.root, 500, 400)
        self.root.resizable(False, False)
        self.current_user = None

        username = load_session()
        if username:
            user = session.query(User).filter_by(username=username).first()
            if user:
                self.current_user = user

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root,
                 text="WISIELEC",
                 font=("Segoe UI", 24, "bold"),
                 fg="white", bg="#333").pack(pady=20, fill="x")

        self.user_label = tk.Label(self.root,
                                   text=f"Zalogowany: {self.current_user.username}"
                                        if self.current_user else "Niezalogowany",
                                   font=('Segoe UI', 10, 'italic'))
        self.user_label.pack(pady=5)

        tk.Button(self.root,
                  text="Nowa Gra",
                  command=self.start_game,
                  **get_button_style()).pack(pady=5)

        self.auth_button = tk.Button(self.root,
                                     text="Wyloguj" if self.current_user else "Logowanie",
                                     command=self._on_auth,
                                     **get_button_style())
        self.auth_button.pack(pady=5)

        tk.Button(self.root,
                  text="Tabela Wyników",
                  command=self.open_scoreboard,
                  **get_button_style()).pack(pady=5)

        tk.Button(self.root,
                  text="Ustawienia Gry",
                  command=self.open_settings,
                  **get_button_style()).pack(pady=5)

        tk.Button(self.root,
                  text="Wyjście",
                  command=self.root.quit,
                  **get_button_style()).pack(pady=20)

    def _on_auth(self):
        if self.current_user:
            clear_session()
            self.current_user = None
            messagebox.showinfo("Wylogowano", "Zostałeś wylogowany.")
            self._refresh_ui()
        else:
            def on_success(user):
                self.current_user = user
                self._refresh_ui()

            LoginWindow(self.root, on_success=on_success)

    def _refresh_ui(self):
        self.user_label.config(text=f"Zalogowany: {self.current_user.username}"
        if self.current_user else "Niezalogowany")
        self.auth_button.config(text="Wyloguj" if self.current_user else "Logowanie")

    def start_game(self):
        if not self.current_user:
            messagebox.showwarning("Uwaga", "Musisz być zalogowany, aby rozpocząć grę.")
            return

        self.root.withdraw()
        if settings.get("tryb") == "Dwóch graczy":
            open_player_input_window(menu=self, mode="Dwóch graczy")
        else:
            open_start_config_window(self)

    def open_settings(self):
        open_settings_window(self)

    def open_scoreboard(self):
        open_scoreboard_window()

    def return_to_menu(self):
        self.root.deiconify()







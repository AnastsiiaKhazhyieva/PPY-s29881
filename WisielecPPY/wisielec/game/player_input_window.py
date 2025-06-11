import tkinter as tk
from tkinter import messagebox

from game_window import GameWindow
from global_settings import settings
from global_settings import WindowManager
import re
from global_settings import get_button_style

def open_player_input_window(menu, mode, score=0, error_count=0):
    win = tk.Toplevel()
    win.title("Gracz 1 – Podaj hasło")
    WindowManager.center_window(win, 300, 200)

    tk.Label(win, text="Wpisz hasło dla Gracza 2:", font=(settings["czcionka"], 14)).pack(pady=10)
    entry = tk.Entry(win, font=(settings["czcionka"], 14))
    entry.pack(pady=10)

    def submit():
        word = entry.get().strip()
        if not word:
            messagebox.showwarning("Błąd", "Pole nie może być puste.")
            return
        if not re.fullmatch(r"[a-ząćęłńóśźż]+", word):
            messagebox.showwarning(
                "Błąd",
                "Hasło może zawierać tylko małe litery polskiego alfabetu (bez spacji, cyfr, znaków specjalnych)."
            )
            return

        win.destroy()
        game_win = tk.Toplevel()
        GameWindow(
            root=game_win,
            category_name="Gracz 1",
            game_mode=mode,
            on_exit=menu.return_to_menu,
            custom_word=word.upper(),
            user=menu.current_user,
            score=score,
            error_count=error_count,
            multiplayer=True
        )

    tk.Button(win, text="Zatwierdź", command=submit, **get_button_style()).pack(pady=10)

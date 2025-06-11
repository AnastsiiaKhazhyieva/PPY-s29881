import tkinter as tk
from tkinter import ttk
from global_settings import settings
from global_settings import WindowManager

def open_settings_window():
    window = tk.Toplevel()
    window.title("Ustawienia gry")
    WindowManager.center_window(window, 300, 400)

    tk.Label(window, text="Wybierz ustawienia:", font=("Arial", 16)).pack(pady=10)

    tk.Label(window, text="Styl interfejsu:").pack()
    style_var = tk.StringVar(value=settings.get("styl_interfejsu", "Niebieski"))
    ttk.Combobox(window, textvariable=style_var,
                 values=["Różowy", "Żółty", "Niebieski"], state="readonly").pack()

    tk.Label(window, text="Rodzaj czcionki:").pack()
    font_var = tk.StringVar(value=settings.get("czcionka", "Arial"))
    ttk.Combobox(window, textvariable=font_var,
                 values=["Arial", "Courier", "Comic Sans", "Verdana", "Tahoma"], state="readonly").pack()

    tk.Label(window, text="Styl wisielca:").pack()
    hangman_var = tk.StringVar(value=settings.get("styl_wisielca", "classic"))
    ttk.Combobox(window, textvariable=hangman_var,
                 values=["classic", "cartoon"], state="readonly").pack()

    def submit_settings():
        settings["styl_interfejsu"] = style_var.get()
        settings["czcionka"] = font_var.get()
        settings["styl_wisielca"] = hangman_var.get()
        window.destroy()

    tk.Button(window, text="Zatwierdź", command=submit_settings).pack(pady=20)
import tkinter as tk
from category_window import CategoryWindow
from player_input_window import open_player_input_window
from global_settings import settings
from global_settings import WindowManager
from global_settings import get_button_style

def open_start_config_window(menu):
    window = tk.Toplevel()
    window.title("Konfiguracja gry")
    window.protocol("WM_DELETE_WINDOW", menu.return_to_menu)
    WindowManager.center_window(window, 300, 350)

    tk.Label(window, text="Konfiguruj nową grę", font=(settings["czcionka"], 16)).pack(pady=10)

    players_frame = tk.LabelFrame(window, text="Ilość graczy:")
    players_frame.pack(pady=5, padx=10, fill="x")

    players_var = tk.StringVar(value="1 gracz")

    def on_players_change():
        if players_var.get() == "1 gracz":
            length_frame.pack(pady=5, padx=10, fill="x")
        else:
            length_frame.pack_forget()

    tk.Radiobutton(players_frame, text="1 gracz", variable=players_var,
                   value="1 gracz", indicatoron=0, command=on_players_change).pack(side="left", expand=True, fill="x")
    tk.Radiobutton(players_frame, text="2 graczy", variable=players_var,
                   value="2 graczy", indicatoron=0, command=on_players_change).pack(side="left", expand=True, fill="x")

    mode_frame = tk.LabelFrame(window, text="Tryb gry:")
    mode_frame.pack(pady=5, padx=10, fill="x")

    mode_var = tk.StringVar(value="Normalny")

    tk.Radiobutton(mode_frame, text="Normalny", variable=mode_var,
                   value="Normalny", indicatoron=0).pack(side="left", expand=True, fill="x")
    tk.Radiobutton(mode_frame, text="Na czas", variable=mode_var,
                   value="Na czas", indicatoron=0).pack(side="left", expand=True, fill="x")

    length_frame = tk.LabelFrame(window, text="Długość hasła:")

    length_var = tk.StringVar(value="dowolna")

    tk.Radiobutton(length_frame, text="dowolna", variable=length_var,
                   value="dowolna", indicatoron=0).pack(side="left", expand=True, fill="x")
    tk.Radiobutton(length_frame, text="do 7", variable=length_var,
                   value="do 7", indicatoron=0).pack(side="left", expand=True, fill="x")
    tk.Radiobutton(length_frame, text="powyżej 7", variable=length_var,
                   value="powyzej 7", indicatoron=0).pack(side="left", expand=True, fill="x")

    on_players_change()

    def submit():
        settings["ilosc_graczy"] = 1 if players_var.get() == "1 gracz" else 2
        settings["tryb"] = mode_var.get()
        settings["dlugosc_hasla"] = length_var.get()

        window.destroy()

        if settings["ilosc_graczy"] == 1:
            cat_win = tk.Toplevel()
            CategoryWindow(cat_win, settings["tryb"], menu)
        else:
            open_player_input_window(menu, settings["tryb"])

    tk.Button(window, text="Zatwierdź", command=submit, **get_button_style()).pack(pady=20)



import tkinter as tk
from model_db import GameResult
from db_engine import session
from global_settings import WindowManager

def open_scoreboard_window():
    window = tk.Toplevel()
    window.title("Tabela wyników")
    window.geometry("400x400")
    WindowManager.center_window(window, 400, 400)

    tk.Label(window, text="Najlepsze gry", font=("Arial", 16)).pack(pady=10)

    frame = tk.Frame(window)
    frame.pack()

    headers = ["Gracz", "Punkty"]
    for col, text in enumerate(headers):
        tk.Label(frame, text=text, font=("Arial", 12, "bold"), borderwidth=2, relief="groove", width=18).grid(row=0, column=col)

    results = session.query(GameResult).order_by(GameResult.points.desc()).limit(50).all()

    for row, result in enumerate(results, start=1):
        tk.Label(frame, text=result.username, width=18).grid(row=row, column=0)
        tk.Label(frame, text=str(result.points), width=18).grid(row=row, column=1)


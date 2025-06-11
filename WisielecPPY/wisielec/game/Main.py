import tkinter as tk
from menu import MainMenu
from db_engine import init_db

if __name__ == '__main__':
    try:
        init_db()
        root = tk.Tk()
        MainMenu(root)
        root.mainloop()
    except Exception as e:
        print(f"Błąd: {e}")
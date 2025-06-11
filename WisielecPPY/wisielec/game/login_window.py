import tkinter as tk
from tkinter import messagebox
from authorization import login_user
from register_window import RegisterWindow
from settings_window import WindowManager
from global_settings import get_button_style

class LoginWindow:
    def __init__(self, master, on_success):
        self.top = tk.Toplevel(master)
        self.top.title("Logowanie")
        WindowManager.center_window(self.top,300, 250)
        self.top.resizable(False, False)

        self.on_success = on_success
        self.top.protocol("WM_DELETE_WINDOW", self.top.destroy)

        tk.Label(self.top, text="Nazwa użytkownika:").pack(pady=5)
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack(pady=5)

        tk.Label(self.top, text="Hasło:").pack(pady=5)
        self.password_entry = tk.Entry(self.top, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.top, text="Zaloguj", command=self.attempt_login, **get_button_style()).pack(pady=15)
        tk.Button(self.top, text="Zarejestruj się", command=self.open_register_window, **get_button_style()).pack()
        tk.Button(self.top, text="Anuluj", command=self.top.destroy, **get_button_style()).pack()

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, result = login_user(username, password)
        if success:
            messagebox.showinfo("Sukces", f"Witaj, {result.username}!")
            self.top.destroy()
            self.on_success(result)
        else:
            messagebox.showerror("Błąd", result)

    def open_register_window(self):
        RegisterWindow(self.top)
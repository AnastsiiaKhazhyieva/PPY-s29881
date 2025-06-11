import tkinter as tk
from tkinter import messagebox
from authorization import register_user
from global_settings import WindowManager
from global_settings import get_button_style

class RegisterWindow:
    def __init__(self, toplevel):
        self.top = tk.Toplevel(toplevel)
        self.top.title("Rejestracja")
        WindowManager.center_window(self.top, 300,250)
        self.top.resizable(False, False)

        tk.Label(self.top, text="Nazwa użytkownika:").pack(pady=5)
        self.username_entry = tk.Entry(self.top)
        self.username_entry.pack(pady=5)

        tk.Label(self.top, text="Hasło:").pack(pady=5)
        self.password_entry = tk.Entry(self.top, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.top, text="Zarejestruj", command=self.attempt_register, **get_button_style()).pack(pady=15)
        tk.Button(self.top, text="Anuluj", command=self.top.destroy, **get_button_style()).pack()


    def attempt_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = register_user(username, password)
        if success:
            messagebox.showinfo("Sukces", message)
            self.top.destroy()
        else:
            messagebox.showerror("Błąd", message)

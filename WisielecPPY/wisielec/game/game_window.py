import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import random
from model_db import Category, Password, GameResult
from db_engine import session
from global_settings import settings, WindowManager, get_button_style

LETTERS = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUVWXYZŹŻ"
IMAGE_SIZE = (200, 300)
MAX_ERRORS = 7
INITIAL_TIME = 30

class GameWindow:
    def __init__(self, root, category_name, game_mode, on_exit, custom_word=None, user=None, score=0, error_count=0, multiplayer=False):
        self.root = root
        self.category_name = category_name
        self.game_mode = game_mode
        self.on_exit = on_exit
        self.user = user
        self.points = score
        self.error_count = error_count
        self.multiplayer = multiplayer
        self.time_left = INITIAL_TIME
        self.timer_id = None

        self.root.title("Wisielec")
        WindowManager.center_window(self.root, 700, 450)

        self.setup_ui()
        self.setup_word(custom_word)
        self.create_keyboard()
        if self.game_mode == "Na czas":
            self.update_timer()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=0, sticky="n")

        self.image_label = tk.Label(self.main_frame)
        self.image_label.grid(row=0, column=1, padx=20, pady=20)
        self.update_hangman_image()

        info = f"Kategoria: {self.category_name}   |   Tryb: {self.game_mode}   |   Punkty: {self.points}"
        tk.Label(self.right_frame, text=info, anchor="e", font=(settings["czcionka"], 10)).pack(anchor="ne", padx=10, pady=10)

        if self.game_mode == "Na czas":
            self.timer_label = tk.Label(self.right_frame, text=f"Czas: {self.time_left}", font=(settings["czcionka"], 12))
            self.timer_label.pack(anchor="ne", padx=10)

        self.word_label = tk.Label(self.right_frame, font=(settings["czcionka"], 28))
        self.word_label.pack(pady=40)

        self.keyboard_frame = tk.Frame(self.right_frame)
        self.keyboard_frame.pack()

    def setup_word(self, custom_word):
        if custom_word:
            self.word = custom_word.upper()
        else:
            category = session.query(Category).filter_by(name=self.category_name).first()
            words = session.query(Password).filter_by(category_id=category.id).all()

            if settings["dlugosc_hasla"] == "do 7":
                words = [w for w in words if len(w.word) <= 7]
            elif settings["dlugosc_hasla"] == "powyzej 7":
                words = [w for w in words if len(w.word) > 7]

            if not words:
                messagebox.showerror("Błąd", "Brak słów w tej kategorii!")
                self.root.destroy()
                self.on_exit()
                return

            self.word = random.choice(words).word.upper()

        self.displayed = ["_" for _ in self.word]
        self.letters_guessed = set()
        self.word_label.config(text=" ".join(self.displayed))

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.config(text=f"Czas: {self.time_left}")
        if self.time_left <= 0:
            self.end_game(success=False, reason="Czas się skończył")
        else:
            self.timer_id = self.root.after(1000, self.update_timer)

    def update_hangman_image(self):
        styl = settings.get("styl_wisielca", "classic")
        img_path = Path(__file__).resolve().parent.parent / "images" / styl / f"wisielec{self.error_count}.png"

        if img_path.exists():
            img = Image.open(img_path).resize(IMAGE_SIZE)
            self.wisielec_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.wisielec_image)
        else:
            self.image_label.config(image='')
            print(f"Nie znaleziono pliku obrazka: {img_path}")

    def create_keyboard(self):
        for index, letter in enumerate(LETTERS):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2,
                            command=lambda l=letter: self.check_letter(l), **get_button_style())
            btn.grid(row=index // 9, column=index % 9, padx=3, pady=3)

    def check_letter(self, letter):
        if letter in self.letters_guessed:
            return

        self.letters_guessed.add(letter)
        for widget in self.keyboard_frame.winfo_children():
            if widget.cget("text") == letter:
                widget.config(state="disabled")
                break

        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.displayed[i] = letter
            self.word_label.config(text=" ".join(self.displayed))

            if "_" not in self.displayed:
                self.points += 10
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
                messagebox.showinfo("Wygrana!", f"Brawo! Odgadłeś słowo!\nAktualne punkty: {self.points}")
                self.root.destroy()

                if self.multiplayer:
                    from player_input_window import open_player_input_window
                    open_player_input_window(menu=self.on_exit.__self__, mode=self.game_mode, score=self.points, error_count=self.error_count)
                else:
                    self.next_round()
        else:
            self.error_count += 1
            self.update_hangman_image()
            if self.error_count >= MAX_ERRORS:
                if self.timer_id:
                    self.root.after_cancel(self.timer_id)
                self.end_game(success=False, reason=f"Przegrałeś. Hasło to: {self.word}")

    def next_round(self):
        next_window = tk.Toplevel()
        GameWindow(root=next_window, category_name=self.category_name, game_mode=self.game_mode,
                   on_exit=self.on_exit, user=self.user, score=self.points)
        self.root.destroy()

    def end_game(self, success, reason):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if success:
            self.points += 10
        messagebox.showinfo("Koniec gry", f"{'Brawo!' if success else reason}\nPunkty: {self.points}")
        if self.user:
            self.save_score()
        self.root.destroy()
        self.on_exit()

    def save_score(self):
        result = GameResult(username=self.user.username, points=self.points)
        session.add(result)

        self.user.games_played += 1
        if self.points > 0:
            self.user.games_won += 1
        session.add(self.user)

        session.commit()

        results = session.query(GameResult).order_by(GameResult.id.desc()).all()
        if len(results) > 50:
            for r in results[50:]:
                session.delete(r)
            session.commit()


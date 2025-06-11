class WindowManager:
    @staticmethod
    def center_window(win, width, height):
        screen_w = win.winfo_screenwidth()
        screen_h = win.winfo_screenheight()

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        win.geometry(f"{width}x{height}+{x}+{y}")

settings = {
    "styl_interfejsu": "Niebieski",
    "czcionka": "Arial",
    "styl_wisielca": "classic",
    "ilosc_graczy": 1,
    "tryb": "Normalny",
    "dlugosc_hasla": "dowolna"
}

def get_button_style():
    kolor = settings.get("styl_interfejsu", "Niebieski")
    font = (settings["czcionka"], 12)

    if kolor == "Różowy":
        return {
            'font': font,
            'bg': "#ffb6c1",
            'fg': "#99004d",
            'activebackground': "#ff69b4",
            'activeforeground': "#ffffff",
            'relief': "raised",
            'bd': 2
        }
    elif kolor == "Żółty":
        return {
            'font': font,
            'bg': "#fff176",
            'fg': "#665500",
            'activebackground': "#ffee58",
            'activeforeground': "#000000",
            'relief': "raised",
            'bd': 2
        }
    else:
        return {
            'font': font,
            'bg': "#2a7a8c",
            'fg': "white",
            'activebackground': "#6a8aac",
            'activeforeground': "white",
            'relief': "raised",
            'bd': 2
        }

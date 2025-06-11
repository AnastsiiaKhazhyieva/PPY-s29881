from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model_db import Base, Category, Password

engine = create_engine('sqlite:///wisielec.db')
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    insert_data(session)

def insert_data(session):
    if session.query(Category).first():
        return

    categories = {
        "Zwierzęta": [
            "lew", "tygrys", "słoń", "żyrafa", "kangur",
            "niedźwiedź", "wilk", "lis", "koń", "zebra",
            "małpa", "szop", "delfin", "rekin", "pingwin",
            "foka", "jeż", "wieloryb", "bóbr", "lama"
        ],
        "Państwa": [
            "polska", "niemcy", "włochy", "kanada", "egipt",
            "hiszpania", "francja", "grecja", "szwecja", "norwegia",
            "japonia", "chiny", "australia", "brazylia", "meksyk",
            "argentina", "indie", "turcja", "ukraina", "usa"
        ],
        "Owoce": [
            "jabłko", "banan", "gruszka", "pomarańcza", "arbuz",
            "ananas", "mango", "mandarynka", "śliwka", "winogrono",
            "kiwi", "granat", "truskawka", "malina", "jagoda",
            "brzoskwinia", "morela", "cytryna", "limonka", "kokos"
        ],
        "Sporty": [
            "piłka", "tenis", "koszykówka", "siatkówka", "boks",
            "bieganie", "narciarstwo", "łyżwiarstwo", "hokej", "rugby",
            "badminton", "szermierka", "karate", "judo", "zapasy",
            "wspinaczka", "golf", "kolarstwo", "pływanie", "skok o tyczce"
        ],
        "Jedzenie": [
            "pizza", "spaghetti", "hamburger", "pierogi", "sushi",
            "nuggetsy", "kanapka", "rosół", "kebab", "sałatka",
            "omlet", "ciasto", "zupa", "gulasz", "nalesniki",
            "tort", "kotlet", "gołąbki", "frytki", "tost"
        ],
        "Informatyka": [
            "algorytm", "programista", "kompilator", "serwer", "baza danych",
            "sieć", "sztuczna inteligencja", "python", "debugowanie", "kod źródłowy",
            "funkcja", "zmienna", "pętla", "biblioteka", "interfejs",
            "system operacyjny", "pamięć ram", "procesor", "linux", "zapora sieciowa"
        ]
    }

    for category, passwords in categories.items():
        cat = Category(name=category)
        session.add(cat)
        session.commit()

        for password in passwords:
            session.add(Password(word=password.lower(), category_id=cat.id))

    session.commit()

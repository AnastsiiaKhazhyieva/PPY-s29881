import bcrypt
from model_db import User
from db_engine import session
import json
from pathlib import Path

SESSION_FILE = Path("session.json")

def register_user(username, password):
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        return False, "Użytkownik już istnieje!"

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(username=username, password=password_hash.decode())
    session.add(new_user)
    session.commit()
    return True, "Użytkownik został zarejestrowany!"

def login_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        save_session(user)
        return True, user
    return False, "Nieprawidłowe hasło lub login"

def save_session(user):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": user.username}, f)

def load_session():
    if SESSION_FILE.exists():
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    return None

def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
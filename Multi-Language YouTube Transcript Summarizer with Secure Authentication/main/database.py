import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    result = cursor.fetchone()
    conn.close()
    return result is not None

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "skillsift.db")

def connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # RESUMES
    c.execute("""
    CREATE TABLE IF NOT EXISTS resumes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        mobile TEXT,
        filename TEXT,
        filepath TEXT,
        skills TEXT,
        score INTEGER,
        pages INTEGER,
        timestamp TEXT
    )
    """)

    # FEEDBACK
    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        rating INTEGER,
        comment TEXT,
        timestamp TEXT
    )
    """)

    # DEFAULT USERS
    c.execute("INSERT OR IGNORE INTO users VALUES('admin@gmail.com','admin123','admin')")
    c.execute("INSERT OR IGNORE INTO users VALUES('user@gmail.com','user123','user')")

    conn.commit()
    conn.close()
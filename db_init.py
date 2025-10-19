# Jalankan sekali untuk membuat DB
import sqlite3
from config import DATABASE

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    type TEXT NOT NULL, -- 'in' atau 'out'
    lat REAL,
    lon REAL,
    photo_path TEXT,
    note TEXT,
    duration_minutes INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)''')

conn.commit()
conn.close()
print('DB initialized')

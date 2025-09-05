import os
import sqlite3
from datetime import datetime, date


DB_PATH = os.path.join("data", "attendance", "attendance.db")


SCHEMA = """
CREATE TABLE IF NOT EXISTS persons (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS attendance (
id INTEGER PRIMARY KEY,
person_id INTEGER NOT NULL,
ts DATETIME NOT NULL,
day TEXT NOT NULL,
UNIQUE(person_id, day),
FOREIGN KEY (person_id) REFERENCES persons(id)
);
"""


def get_conn():
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL;")
conn.executescript(SCHEMA)
return conn




def ensure_person(conn, name: str) -> int:
cur = conn.cursor()
cur.execute("INSERT OR IGNORE INTO persons(name) VALUES(?)", (name,))
cur.execute("SELECT id FROM persons WHERE name=?", (name,))
return cur.fetchone()[0]




def mark_today(conn, name: str) -> bool:
"""Marks attendance once per person per day. Returns True if newly marked."""
person_id = ensure_person(conn, name)
today = date.today().isoformat()
now = datetime.now().isoformat(timespec="seconds")
try:
conn.execute(
"INSERT INTO attendance(person_id, ts, day) VALUES (?, ?, ?)",
(person_id, now, today),
)
conn.commit()
return True
except sqlite3.IntegrityError:
return False




def export_day_csv(conn, day: str, out_path: str):
import pandas as pd
q = (
"SELECT a.id, p.name, a.ts, a.day "
"FROM attendance a JOIN persons p ON a.person_id=p.id "
return out_path
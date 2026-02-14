from datetime import datetime
from services.db import get_connection

def add_shop(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO shop (name, created_at) VALUES (?, ?)",
        (name, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_shops():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM shop ORDER BY name")
    shops = [r[0] for r in cur.fetchall()]
    conn.close()
    return shops

def delete_shop(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shop WHERE name=?", (name,))
    conn.commit()
    conn.close()

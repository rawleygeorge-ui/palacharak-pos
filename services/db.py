import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "pos.db"

_conn = None


def get_connection():
    global _conn

    DB_PATH.parent.mkdir(exist_ok=True)

    if _conn is None:
        _conn = sqlite3.connect(DB_PATH)
        return _conn

    # 🔑 Detect CLOSED connection and recreate it
    try:
        _conn.execute("SELECT 1")
    except sqlite3.ProgrammingError:
        _conn = sqlite3.connect(DB_PATH)

    return _conn


def get_cursor():
    return get_connection().cursor()


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # =================================================
    # OWNER TABLE
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS owner (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT
        )
    """)

    # =================================================
    # SHOP TABLE (LEGACY)
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shop (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            created_at TEXT
        )
    """)

    # =================================================
    # SHOPS TABLE
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            shop_id TEXT PRIMARY KEY,
            shop_name TEXT,
            owner_name TEXT,
            dob TEXT,
            mobile_last4 TEXT,
            town TEXT
        )
    """)

    # =================================================
    # USERS TABLE
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            shop_id TEXT,
            owner_name TEXT,
            created_at TEXT
        )
    """)

    # =================================================
    # INVENTORY TABLE
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT,
            item TEXT,
            unit TEXT,
            price REAL
        )
    """)

    # Safe migration
    try:
        cur.execute("ALTER TABLE inventory ADD COLUMN item_norm TEXT")
    except sqlite3.OperationalError:
        pass

    cur.execute("""
        UPDATE inventory
        SET item_norm = LOWER(TRIM(item))
        WHERE item_norm IS NULL
    """)

    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_inventory_unique
        ON inventory (shop_id, item_norm, unit)
    """)

    # =================================================
    # PRICE HISTORY
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id TEXT,
            item TEXT,
            unit TEXT,
            old_price REAL,
            new_price REAL,
            effective_date TEXT
        )
    """)

    # =================================================
    # BILLS TABLE
    # =================================================
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_no TEXT UNIQUE,
            shop_id TEXT,
            shop_name TEXT,
            user_name TEXT,
            bill_date TEXT,
            total REAL,
            payment_mode TEXT,
            paid_amount REAL,
            balance REAL
        )
    """)

    conn.commit()

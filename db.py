import sqlite3
from paths import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# =================================================
# SHOPS TABLE
# =================================================
cur.execute("""
CREATE TABLE IF NOT EXISTS shops (
    shop_id TEXT PRIMARY KEY,
    shop_name TEXT,
    owner_name TEXT,
    dob TEXT,
    mobile TEXT,
    town TEXT,
    owner_uid TEXT
)
""")

# --- SAFE MIGRATION (for existing DBs without owner_uid) ---
cur.execute("PRAGMA table_info(shops)")
columns = [col[1] for col in cur.fetchall()]
if "owner_uid" not in columns:
    cur.execute("ALTER TABLE shops ADD COLUMN owner_uid TEXT")

# =================================================
# USERS TABLE
# =================================================
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id TEXT,
    username TEXT UNIQUE
)
""")

# --- SAFE MIGRATION FOR USERS TABLE ---
cur.execute("PRAGMA table_info(users)")
user_columns = [col[1] for col in cur.fetchall()]

if "username" not in user_columns:
    cur.execute("ALTER TABLE users ADD COLUMN username TEXT")

if "shop_id" not in user_columns:
    cur.execute("ALTER TABLE users ADD COLUMN shop_id TEXT")

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

# =================================================
# REVENUE TABLE
# =================================================
cur.execute("""
CREATE TABLE IF NOT EXISTS revenue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shop_id TEXT,
    date TEXT,
    particulars TEXT,
    description TEXT,
    amount REAL
)
""")

# =================================================
# PRICE HISTORY TABLE (audit trail)
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

# --- SAFE MIGRATIONS FOR OLDER DATABASES ---
cur.execute("PRAGMA table_info(price_history)")
ph_columns = [col[1] for col in cur.fetchall()]

if "unit" not in ph_columns:
    cur.execute("ALTER TABLE price_history ADD COLUMN unit TEXT")

if "effective_date" not in ph_columns:
    cur.execute("ALTER TABLE price_history ADD COLUMN effective_date TEXT")

conn.commit()

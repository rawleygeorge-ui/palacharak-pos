from datetime import datetime
from services import db
import hashlib


def owner_exists():
    cur = db.get_cursor()
    row = cur.execute(
        "SELECT 1 FROM owner LIMIT 1"
    ).fetchone()
    return row is not None


def verify_owner(username, password):
    cur = db.get_cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    row = cur.execute(
        """
        SELECT id
        FROM owner
        WHERE username = ? AND password_hash = ?
        """,
        (username, password_hash),
    ).fetchone()

    return row is not None


def create_owner(username, password):
    cur = db.get_cursor()

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    created_at = datetime.now().isoformat(timespec="seconds")

    cur.execute(
        """
        INSERT INTO owner (username, password_hash, created_at)
        VALUES (?, ?, ?)
        """,
        (username, password_hash, created_at),
    )

    # Commit via shared connection
    db.get_connection().commit()

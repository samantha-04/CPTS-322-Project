import os
import sqlite3
import secrets
import hashlib
from typing import Optional, Dict, Any

# Default DB path: ../../data/users.db relative to this file
DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.db'))


def _connect(path: Optional[str] = None):
    p = path or DEFAULT_DB_PATH
    d = os.path.dirname(p)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    conn = sqlite3.connect(p, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: Optional[str] = None) -> None:
    """Initialize database and create tables if they don't exist."""
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            email TEXT UNIQUE,
            salt TEXT,
            pwd_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()


def get_user_by_email(email: str, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = ?', (email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def get_user_by_id(user_id: str, path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)


def create_user_oauth(username: str, email: str, path: Optional[str] = None) -> Dict[str, Any]:
    """Create a user record for OAuth-created users (no password)."""
    import secrets, hashlib
    user_id = hashlib.sha256(f"{email}{secrets.token_hex(8)}".encode()).hexdigest()[:8]
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (id, username, email) VALUES (?, ?, ?)', (user_id, username, email))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id, path)


def create_user_with_password(username: str, email: str, salt_hex: str, pwd_hash_hex: str, path: Optional[str] = None) -> Dict[str, Any]:
    import secrets, hashlib
    user_id = hashlib.sha256(f"{email}{secrets.token_hex(8)}".encode()).hexdigest()[:8]
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (id, username, email, salt, pwd_hash) VALUES (?, ?, ?, ?, ?)',
                (user_id, username, email, salt_hex, pwd_hash_hex))
    conn.commit()
    conn.close()
    return get_user_by_id(user_id, path)


def create_session(token: str, user_id: str, path: Optional[str] = None) -> None:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO sessions (token, user_id) VALUES (?, ?)', (token, user_id))
    conn.commit()
    conn.close()


def get_all_sessions(path: Optional[str] = None) -> Dict[str, str]:
    """Return all sessions as a dict token -> user_id"""
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('SELECT token, user_id FROM sessions')
    rows = cur.fetchall()
    conn.close()
    return {row['token']: row['user_id'] for row in rows}


def get_all_users(path: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    conn.close()
    return {row['id']: dict(row) for row in rows}


def hash_password(password: str) -> Dict[str, str]:
    """Hash a password using PBKDF2-HMAC-SHA256 and return hex salt and hash."""
    salt = secrets.token_bytes(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return {'salt': salt.hex(), 'hash': pwd_hash.hex()}


def verify_password(stored_salt_hex: str, stored_hash_hex: str, password: str) -> bool:
    salt = bytes.fromhex(stored_salt_hex)
    check = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000).hex()
    return secrets.compare_digest(check, stored_hash_hex)


def create_user_with_password_plain(username: str, email: str, password: str, path: Optional[str] = None) -> Dict[str, Any]:
    p = hash_password(password)
    return create_user_with_password(username, email, p['salt'], p['hash'], path)


def get_user_id_by_session(token: str, path: Optional[str] = None) -> Optional[str]:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM sessions WHERE token = ?', (token,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return row['user_id']


def delete_session(token: str, path: Optional[str] = None) -> None:
    conn = _connect(path)
    cur = conn.cursor()
    cur.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()


# convenience: initialize DB at import time (no-op if already exists)
init_db()

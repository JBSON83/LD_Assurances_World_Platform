import sqlite3
import os
import secrets
import string
import time
from typing import Dict, List, Optional

# Path toward the same directory as knowledge_vault.db
DB_PATH = os.path.join(os.path.dirname(__file__), "admin_config.db")

class AdminManager:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Initialisation de la base de données admin."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Table pour les configurations (Pixels, etc)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            # Table pour les clés API du site
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_keys (
                    token TEXT PRIMARY KEY,
                    name TEXT,
                    created_at INTEGER,
                    last_used INTEGER,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            conn.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def set_setting(self, key: str, value: str):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
            conn.commit()

    def get_all_settings(self) -> Dict[str, str]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM settings")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def generate_api_key(self, name: str) -> str:
        """Génère un nouveau token API sécurisé."""
        alphabet = string.ascii_letters + string.digits
        token = "jem_" + "".join(secrets.choice(alphabet) for _ in range(32))
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO api_keys (token, name, created_at, is_active) VALUES (?, ?, ?, 1)",
                (token, name, int(time.time()))
            )
            conn.commit()
        return token

    def validate_api_key(self, token: str) -> bool:
        """Vérifie si une clé API est valide et active."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_active FROM api_keys WHERE token = ?", (token,))
            row = cursor.fetchone()
            if row and row[0] == 1:
                # Update last used
                cursor.execute("UPDATE api_keys SET last_used = ? WHERE token = ?", (int(time.time()), token))
                conn.commit()
                return True
        return False

    def list_api_keys(self) -> List[Dict]:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT token, name, created_at, last_used, is_active FROM api_keys")
            return [dict(row) for row in cursor.fetchall()]

    def revoke_api_key(self, token: str):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE api_keys SET is_active = 0 WHERE token = ?", (token,))
            conn.commit()

# Instance globale pour le serveur
admin_manager = AdminManager()

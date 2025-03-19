import sqlite3
import os
from homeassistant.core import HomeAssistant

class FleetDatabase:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.db_path = hass.config.path("fleet_charging.db")

    async def initialize(self):
        if not os.path.exists(self.db_path):
            self._create_database()

    def _create_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE vehicles (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )""")
            cursor.execute("""
                CREATE TABLE users (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )""")
            cursor.execute("""
                CREATE TABLE wallboxes (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )""")
            cursor.execute("""
                CREATE TABLE sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    vehicle_id TEXT,
                    user_id TEXT,
                    wallbox_id TEXT,
                    energy_consumed REAL DEFAULT 0.0
                )""")
            conn.commit()

    # Pridanie vozidla
    async def add_vehicle(self, vehicle_id, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO vehicles (id, name) VALUES (?, ?)", (vehicle_id, name))
            conn.commit()

    # Pridanie užívateľa
    async def add_user(self, user_id, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))
            conn.commit()

    # Pridanie Wallboxu
    async def add_wallbox(self, wallbox_id, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO wallboxes (id, name) VALUES (?, ?)", (wallbox_id, name))
            conn.commit()

    # Zaznamenanie nabíjacej relácie
    async def log_session(self, vehicle_id, user_id, wallbox_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sessions (vehicle_id, user_id, wallbox_id)
                VALUES (?, ?, ?)
            """, (vehicle_id, user_id, wallbox_id))
            conn.commit()

    # Aktualizácia spotreby energie pre reláciu
    async def update_energy_usage(self, session_id, energy):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE sessions
                SET energy_consumed = ?
                WHERE id = ?
            """, (energy, session_id))
            conn.commit()

    # Získanie poslednej relácie nabíjania
    async def get_latest_session(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT vehicle_id, user_id, wallbox_id FROM sessions
                ORDER BY timestamp DESC LIMIT 1
            """)
            row = cursor.fetchone()
            return {"vehicle_id": row[0], "user_id": row[1], "wallbox_id": row[2]} if row else None


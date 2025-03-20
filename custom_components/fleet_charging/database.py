import sqlite3
import os
from homeassistant.core import HomeAssistant

class FleetDatabase:
    """Trieda na správu databázy pre Fleet Charging Manager."""

    def __init__(self, hass: HomeAssistant):
        """Inicializácia databázy."""
        self.hass = hass
        self.db_path = hass.config.path("fleet_charging.db")

    async def initialize(self):
        """Vytvorenie tabuľky, ak neexistuje."""
        if not os.path.exists(self.db_path):
            self._create_database()

    def _create_database(self):
        """Definícia štruktúry databázy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )""")
            cursor.execute("""
                CREATE TABLE vehicles (
                    id TEXT PRIMARY KEY,
                    name TEXT
                )""")
            cursor.execute("""
                CREATE TABLE wallboxes (
                    id TEXT PRIMARY KEY,
                    location TEXT
                )""")
            cursor.execute("""
                CREATE TABLE sessions (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    vehicle_id TEXT,
                    user_id TEXT,
                    wallbox_id TEXT
                )""")
            conn.commit()

    async def add_user(self, user_id, name):
        """Pridanie užívateľa do databázy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))
            conn.commit()

    async def add_vehicle(self, vehicle_id, name):
        """Pridanie vozidla do databázy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO vehicles (id, name) VALUES (?, ?)", (vehicle_id, name))
            conn.commit()

    async def add_wallbox(self, wallbox_id, location):
        """Pridanie wallboxu do databázy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO wallboxes (id, location) VALUES (?, ?)", (wallbox_id, location))
            conn.commit()

    async def assign_vehicle(self, user_id, vehicle_id):
        """Priradenie užívateľa k vozidlu."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET assigned_vehicle = ? WHERE id = ?", (vehicle_id, user_id))
            conn.commit()

    async def set_wallbox(self, vehicle_id, wallbox_id):
        """Priradenie wallboxu k vozidlu."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE vehicles SET assigned_wallbox = ? WHERE id = ?", (wallbox_id, vehicle_id))
            conn.commit()

    async def get_all_users(self):
        """Získanie zoznamu užívateľov."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

    async def get_all_vehicles(self):
        """Získanie zoznamu vozidiel."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles")
            return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

    async def get_all_wallboxes(self):
        """Získanie zoznamu wallboxov."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wallboxes")
            return [{"id": row[0], "location": row[1]} for row in cursor.fetchall()]

    async def log_session(self, vehicle_id, user_id, wallbox_id):
        """Uloženie nabíjacej relácie do databázy."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (vehicle_id, user_id, wallbox_id) VALUES (?, ?, ?)",
                (vehicle_id, user_id, wallbox_id)
            )
            conn.commit()

    async def get_all_sessions(self):
        """Získanie zoznamu nabíjacích relácií."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions")
            return [{"timestamp": row[0], "vehicle_id": row[1], "user_id": row[2], "wallbox_id": row[3]} for row in cursor.fetchall()]

    async def generate_daily_report(self):
        """Vytvorí sumár nabíjacích relácií za posledných 24 hodín."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT vehicle_id, user_id, COUNT(*) as sessions
                FROM sessions
                WHERE timestamp >= datetime('now', '-1 day')
                GROUP BY vehicle_id, user_id
            """)
            return [{"vehicle": row[0], "user": row[1], "sessions": row[2]} for row in cursor.fetchall()]

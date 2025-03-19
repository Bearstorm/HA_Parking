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
                CREATE TABLE sessions (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    vehicle_id TEXT,
                    user_id TEXT
                )""")
            cursor.execute("""
                CREATE TABLE wallbox_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    vehicle_id TEXT,
                    wallbox_id TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(vehicle_id) REFERENCES vehicles(id)
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

    # Pridanie Wallboxu k vozidlu a užívateľovi
    async def assign_wallbox(self, user_id, vehicle_id, wallbox_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wallbox_assignments (user_id, vehicle_id, wallbox_id) VALUES (?, ?, ?)",
                (user_id, vehicle_id, wallbox_id)
            )
            conn.commit()

    # Získanie priradených Wallboxov
    async def get_assigned_wallboxes(self, user_id, vehicle_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT wallbox_id FROM wallbox_assignments WHERE user_id = ? AND vehicle_id = ?",
                (user_id, vehicle_id)
            )
            rows = cursor.fetchall()
            return [row[0] for row in rows] if rows else []


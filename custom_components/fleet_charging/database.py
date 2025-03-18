import sqlite3
import os
from homeassistant.core import HomeAssistant

class FleetDatabase:
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.db_path = hass.config.path("fleet_charging.db")

    async def initialize(self):
        if not os.path.exists(self.db_path):
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
                conn.commit()

    async def get_vehicle(self, vehicle_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
            row = cursor.fetchone()
            return {"id": row[0], "name": row[1]} if row else None

    async def get_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return {"id": row[0], "name": row[1]} if row else None

    async def log_session(self, vehicle_id, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (vehicle_id, user_id) VALUES (?, ?)",
                (vehicle_id, user_id)
            )
            conn.commit()


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
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    vehicle_id TEXT,
                    user_id TEXT,
                    wallbox_id TEXT
                )""")
            cursor.execute("""
                CREATE TABLE wallbox_usage (
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    wallbox_id TEXT,
                    vehicle_id TEXT,
                    user_id TEXT,
                    energy_consumed REAL
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

    # Vyhľadanie vozidla
    async def get_vehicle(self, vehicle_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
            row = cursor.fetchone()
            return {"id": row[0], "name": row[1]} if row else None

    # Vyhľadanie užívateľa
    async def get_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return {"id": row[0], "name": row[1]} if row else None

    # Vyhľadanie Wallboxu
    async def get_wallbox(self, wallbox_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wallboxes WHERE id = ?", (wallbox_id,))
            row = cursor.fetchone()
            return {"id": row[0], "name": row[1]} if row else None

    # Logovanie nabíjacej relácie
    async def log_session(self, vehicle_id, user_id, wallbox_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (vehicle_id, user_id, wallbox_id) VALUES (?, ?, ?)",
                (vehicle_id, user_id, wallbox_id)
            )
            conn.commit()

    # Ukladanie spotreby Wallboxu
    async def log_wallbox_usage(self, wallbox_id, vehicle_id, user_id, energy_consumed):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wallbox_usage (wallbox_id, vehicle_id, user_id, energy_consumed) VALUES (?, ?, ?, ?)",
                (wallbox_id, vehicle_id, user_id, energy_consumed)
            )
            conn.commit()

    # Generovanie denného reportu nabíjania
    async def generate_daily_report(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date(timestamp), wallbox_id, vehicle_id, user_id, SUM(energy_consumed)
                FROM wallbox_usage
                GROUP BY date(timestamp), wallbox_id, vehicle_id, user_id
                ORDER BY date(timestamp) DESC LIMIT 10
            """)
            rows = cursor.fetchall()
            report = "\n".join(
                [f"{date}: Wallbox {wb} - Vehicle {vid} - User {uid} ({energy:.2f} kWh)"
                 for date, wb, vid, uid, energy in rows]
            )
            return report if report else "Žiadne dáta"

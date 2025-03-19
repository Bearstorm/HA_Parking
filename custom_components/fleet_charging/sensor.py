from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
from .database import FleetDatabase

async def async_setup_entry(hass, config_entry, async_add_entities):
    db = hass.data["fleet_charging"]["db"]
    async_add_entities([
        ChargingSessionSensor(hass, db),
        WallboxEnergySensor(hass, db),
        ChargingStatisticsSensor(hass, db)
    ])

class ChargingSessionSensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Aktuálna relácia nabíjania"
        self._attr_state = "Žiadna aktívna relácia"
        async_track_time_interval(hass, self.async_update, timedelta(seconds=30))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        session = await self._db.get_latest_session()
        if session:
            vehicle = session.get('vehicle_id')
            user = session.get('user_id')
            wallbox = session.get('wallbox_id')
            self._attr_state = f"Vozidlo: {vehicle}, Používateľ: {user}, Wallbox: {wallbox}"
        else:
            self._attr_state = "Žiadna aktívna relácia"

class WallboxEnergySensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Spotreba Wallboxu"
        self._attr_state = "Neznáme"
        async_track_time_interval(hass, self.async_update, timedelta(minutes=1))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        energy_sensor = self._hass.states.get("sensor.wallbox_energy")
        if energy_sensor:
            self._attr_state = f"{energy_sensor.state} kWh"
        else:
            self._attr_state = "Dáta nie sú dostupné"

class ChargingStatisticsSensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Štatistiky nabíjania"
        self._attr_state = "Neznáme"
        async_track_time_interval(hass, self.async_update, timedelta(minutes=60))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        with sqlite3.connect(self._db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(energy_consumed) FROM sessions WHERE timestamp >= datetime('now', '-30 days')
            """)
            total_energy = cursor.fetchone()[0]
            self._attr_state = f"{total_energy:.2f} kWh" if total_energy else "0 kWh"

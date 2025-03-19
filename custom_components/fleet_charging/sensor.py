from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
from .database import FleetDatabase

async def async_setup_entry(hass, config_entry, async_add_entities):
    db = hass.data["fleet_charging"]["db"]
    async_add_entities([
        ChargingSessionSensor(hass, db),
        WallboxEnergySensor(hass, db),
        WallboxStatusSensor(hass, db)
    ])

# 🔋 Senzor aktuálnej nabíjacej relácie
class ChargingSessionSensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Aktuálna nabíjacia relácia"
        self._attr_state = "Žiadna aktívna relácia"
        async_track_time_interval(hass, self.async_update, timedelta(seconds=30))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        session = await self._db.get_latest_session()
        if session:
            vehicle = session.get('vehicle_name')
            user = session.get('user_name')
            wallbox = session.get('wallbox_name')
            self._attr_state = f"{vehicle} - {user} (Wallbox: {wallbox})"
        else:
            self._attr_state = "Žiadna aktívna relácia"

# ⚡ Senzor spotreby Wallboxu
class WallboxEnergySensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Celková spotreba Wallboxu"
        self._attr_state = "0 kWh"
        async_track_time_interval(hass, self.async_update, timedelta(minutes=60))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        report = await self._db.generate_daily_report()
        if report:
            self._attr_state = report
        else:
            self._attr_state = "Žiadne dáta"

# 🚦 Senzor stavu Wallboxu (autorizácia, kábel, nabíjanie)
class WallboxStatusSensor(SensorEntity):
    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Stav Wallboxu"
        self._attr_state = "Neznámy"
        async_track_time_interval(hass, self.async_update, timedelta(seconds=10))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        wallbox_data = self._hass.states.get("sensor.05_cion_cp_signal_state")
        if wallbox_data:
            state = wallbox_data.state
            if state == "1":
                self._attr_state = "Pripravený"
            elif state == "2":
                self._attr_state = "Nabíja"
            elif state == "3":
                self._attr_state = "Porucha"
            else:
                self._attr_state = "Neznámy stav"

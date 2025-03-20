from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
from .database import FleetDatabase

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Inicializácia senzorov pri pridávaní integrácie."""
    db = hass.data["fleet_charging"]["db"]
    async_add_entities([
        ChargingSessionSensor(hass, db),
        DailyReportSensor(hass, db),
        WallboxStatusSensor(hass, db)
    ])

class ChargingSessionSensor(SensorEntity):
    """Senzor pre aktuálnu reláciu nabíjania."""

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
        session = await self._db.get_all_sessions()
        if session:
            session = sessions[-1]  # Použije poslednú reláciu
            vehicle = session.get('vehicle_id')
            user = session.get('user_id')
            self._attr_state = f"{vehicle} - {user}"
        else:
            self._attr_state = "Žiadna aktívna relácia"

class DailyReportSensor(SensorEntity):
    """Senzor pre denný report nabíjania."""

    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Denný report nabíjania"
        self._attr_state = "Čaká sa na prvý report"
        async_track_time_interval(hass, self.async_update, timedelta(minutes=60))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        self._attr_state = await self._db.get_all_sessions()


class WallboxStatusSensor(SensorEntity):
    """Senzor pre stav Wallboxu a nabíjania."""

    def __init__(self, hass, db: FleetDatabase):
        self._hass = hass
        self._db = db
        self._attr_name = "Stav Wallboxu"
        self._attr_state = "Neznámy"
        async_track_time_interval(hass, self.async_update, timedelta(seconds=30))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        wallbox_status = self._hass.states.get("sensor.05_cion_cp_signal_state")
        if wallbox_status:
            self._attr_state = wallbox_status.state
        else:
            self._attr_state = "Neznámy"


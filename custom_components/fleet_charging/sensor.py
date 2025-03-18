from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([ChargingSessionSensor(hass), DailyReportSensor(hass)])

class ChargingSessionSensor(SensorEntity):
    def __init__(self, hass):
        self._hass = hass
        self._attr_name = "Aktuálna relácia nabíjania"
        self._attr_state = "Žiadna aktívna relácia"
        async_track_time_interval(hass, self.async_update, timedelta(seconds=30))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        data = self._hass.data.get("fleet_charging", {})
        vehicle = data.get("current_vehicle")
        user = data.get("current_user")

        if vehicle and user:
            self._attr_state = f"{vehicle['name']} - {user['name']}"
        else:
            self._attr_state = "Žiadna aktívna relácia"

class DailyReportSensor(SensorEntity):
    def __init__(self, hass):
        self._hass = hass
        self._attr_name = "Denný report nabíjania"
        self._attr_state = "Čaká sa na prvý report"
        async_track_time_interval(hass, self.async_update, timedelta(minutes=60))

    @property
    def state(self):
        return self._attr_state

    async def async_update(self, now=None):
        report = self._hass.states.get("fleet_charging.daily_report")
        if report:
            self._attr_state = report.state
        else:
            self._attr_state = "Report nie je dostupný"


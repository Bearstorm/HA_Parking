import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .database import FleetDatabase

_LOGGER = logging.getLogger(__name__)
DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config):
    """Registrácia API služieb pre Wallboxy."""
    
    db = FleetDatabase(hass)
    await db.initialize()

    # Spustenie nabíjania
    async def start_charging(call: ServiceCall):
        vehicle_id = call.data.get("vehicle_id")
        wallbox_id = call.data.get("wallbox_id")

        _LOGGER.info(f"Spúšťam nabíjanie pre vozidlo {vehicle_id} na Wallboxe {wallbox_id}")

        hass.states.async_set(f"sensor.{wallbox_id}_charging_authorisation", "on")

        hass.bus.async_fire("fleet_charging.charging_started", {
            "vehicle_id": vehicle_id,
            "wallbox_id": wallbox_id
        })

    hass.services.async_register(DOMAIN, "start_charging", start_charging)

    # Ukončenie nabíjania
    async def stop_charging(call: ServiceCall):
        wallbox_id = call.data.get("wallbox_id")

        _LOGGER.info(f"Ukončujem nabíjanie na Wallboxe {wallbox_id}")

        hass.states.async_set(f"sensor.{wallbox_id}_charging_authorisation", "off")

        hass.bus.async_fire("fleet_charging.charging_stopped", {
            "wallbox_id": wallbox_id
        })

    hass.services.async_register(DOMAIN, "stop_charging", stop_charging)

    # Odomknutie kábla
    async def unlock_cable(call: ServiceCall):
        wallbox_id = call.data.get("wallbox_id")

        _LOGGER.info(f"Odomykám kábel na Wallboxe {wallbox_id}")

        hass.states.async_set(f"sensor.{wallbox_id}_lock_unlock_charging_socket", "unlocked")

        hass.bus.async_fire("fleet_charging.cable_unlocked", {
            "wallbox_id": wallbox_id
        })

    hass.services.async_register(DOMAIN, "unlock_cable", unlock_cable)

    # Nastavenie nabíjacieho prúdu
    async def set_charging_current(call: ServiceCall):
        wallbox_id = call.data.get("wallbox_id")
        current = call.data.get("current")

        _LOGGER.info(f"Nastavujem nabíjací prúd na Wallboxe {wallbox_id} na {current} A")

        hass.states.async_set(f"sensor.{wallbox_id}_charging_current_setting", current)

        hass.bus.async_fire("fleet_charging.charging_current_set", {
            "wallbox_id": wallbox_id,
            "current": current
        })

    hass.services.async_register(DOMAIN, "set_charging_current", set_charging_current)

    return True

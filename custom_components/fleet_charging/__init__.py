import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .database import FleetDatabase
from .reporting import generate_report
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config: dict):
    return True  # Spätne kompatibilné

async def async_setup_entry(hass: HomeAssistant, entry):
    db = FleetDatabase(hass)
    await db.initialize()

    hass.data[DOMAIN] = {
        "db": db,
        "current_vehicle": None,
        "current_user": None,
        "selected_wallbox": None  # Wallbox aktuálne používaný
    }

    # Identifikácia vozidla a užívateľa
    async def handle_identify_vehicle(call: ServiceCall):
        vehicle_id = call.data.get("vehicle_id")
        user_id = call.data.get("user_id")
        wallbox_id = call.data.get("wallbox_id")

        vehicle = await db.get_vehicle(vehicle_id)
        user = await db.get_user(user_id)

        if vehicle and user:
            hass.data[DOMAIN]["current_vehicle"] = vehicle
            hass.data[DOMAIN]["current_user"] = user
            hass.data[DOMAIN]["selected_wallbox"] = wallbox_id  # Uloží aktívny wallbox
            await db.log_session(vehicle_id, user_id, wallbox_id)

            hass.states.async_set(f"{DOMAIN}.current_session", f"{vehicle['name']} - {user['name']} (Wallbox {wallbox_id})")
            hass.bus.async_fire("fleet_charging.identification_successful", {
                "vehicle": vehicle,
                "user": user,
                "wallbox": wallbox_id
            })
            _LOGGER.info(f"Identified: {vehicle['name']} by {user['name']} using Wallbox {wallbox_id}")
        else:
            hass.bus.async_fire("fleet_charging.identification_failed", {
                "vehicle_id": vehicle_id,
                "user_id": user_id
            })
            _LOGGER.warning(f"Identification failed: vehicle_id={vehicle_id}, user_id={user_id}")

    hass.services.async_register(DOMAIN, "identify_vehicle", handle_identify_vehicle)

    # API na autorizáciu wallboxu
    async def handle_wallbox_auth(call: ServiceCall):
        wallbox_id = call.data.get("wallbox_id")
        auth_state = call.data.get("auth_state", "off")  # Zapnutie/vypnutie autorizácie

        if wallbox_id:
            entity_id = f"switch.wallbox_{wallbox_id}_autentifikacia_on_off"
            hass.states.async_set(entity_id, auth_state)
            _LOGGER.info(f"Wallbox {wallbox_id} authorization set to {auth_state}")

    hass.services.async_register(DOMAIN, "set_wallbox_auth", handle_wallbox_auth)

    # API na uzamknutie/odomknutie kábla
    async def handle_wallbox_lock(call: ServiceCall):
        wallbox_id = call.data.get("wallbox_id")
        lock_state = call.data.get("lock_state", "unlocked")

        if wallbox_id:
            entity_id = f"sensor.wallbox_{wallbox_id}_lock_unlock_charging_socket"
            hass.states.async_set(entity_id, lock_state)
            _LOGGER.info(f"Wallbox {wallbox_id} cable lock set to {lock_state}")

    hass.services.async_register(DOMAIN, "set_wallbox_lock", handle_wallbox_lock)

    # Automatické generovanie reportu denne
    async def daily_report(now=None):
        report = await generate_report(db)
        hass.states.async_set(f"{DOMAIN}.daily_report", report)
        _LOGGER.info("Daily report generated")

    async_track_time_interval(hass, daily_report, timedelta(days=1))

    # Inicializácia platformy sensor
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

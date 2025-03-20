import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .database import FleetDatabase
from .reporting import generate_report
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config: dict):
    """Inicializácia integrácie pri zavedení konfigurácie (zachované pre kompatibilitu)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Inicializácia integrácie pri pridaní záznamu do Home Assistant."""
    db = FleetDatabase(hass)
    await db.initialize()

    hass.data[DOMAIN] = {
        "db": db,
        "current_vehicle": None,
        "current_user": None
    }

    # Identifikácia vozidla a užívateľa
    async def handle_identify_vehicle(call: ServiceCall):
        vehicle_id = call.data.get("vehicle_id")
        user_id = call.data.get("user_id")

        vehicle = await db.get_vehicle(vehicle_id)
        user = await db.get_user(user_id)

        if vehicle and user:
            hass.data[DOMAIN]["current_vehicle"] = vehicle
            hass.data[DOMAIN]["current_user"] = user
            await db.log_session(vehicle_id, user_id)
            hass.states.async_set(f"{DOMAIN}.current_session", f"{vehicle['name']} - {user['name']}")
            hass.bus.async_fire("fleet_charging.identification_successful", {
                "vehicle": vehicle,
                "user": user
            })
            _LOGGER.info(f"Identified: {vehicle['name']} by {user['name']}")
        else:
            hass.bus.async_fire("fleet_charging.identification_failed", {
                "vehicle_id": vehicle_id,
                "user_id": user_id
            })
            _LOGGER.warning(f"Identification failed: vehicle_id={vehicle_id}, user_id={user_id}")

    hass.services.async_register(DOMAIN, "identify_vehicle", handle_identify_vehicle)

    # Pridanie vozidla
    async def handle_add_vehicle(call: ServiceCall):
        vehicle_id = call.data.get("vehicle_id")
        name = call.data.get("name")
        await db.add_vehicle(vehicle_id, name)
        _LOGGER.info(f"Vehicle added: {vehicle_id} - {name}")

    hass.services.async_register(DOMAIN, "add_vehicle", handle_add_vehicle)

    # Pridanie užívateľa
    async def handle_add_user(call: ServiceCall):
        user_id = call.data.get("user_id")
        name = call.data.get("name")
        await db.add_user(user_id, name)
        _LOGGER.info(f"User added: {user_id} - {name}")

    hass.services.async_register(DOMAIN, "add_user", handle_add_user)

    # Automatické generovanie reportu denne
    async def daily_report(now=None):
        report = await generate_report(db)
        hass.states.async_set(f"{DOMAIN}.daily_report", report)
        _LOGGER.info("Daily report generated")

    async_track_time_interval(hass, daily_report, timedelta(days=1))

    # Inicializácia platformy sensor
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Odstránenie záznamu z Home Assistant."""
    return await hass.config_entries.async_unload(entry)

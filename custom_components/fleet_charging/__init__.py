import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .database import FleetDatabase
from .reporting import generate_report
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config: dict):
    db = FleetDatabase(hass)
    await db.initialize()

    hass.data[DOMAIN] = {
        "db": db,
        "current_vehicle": None,
        "current_user": None
    }

    # Identifikácia vozidla
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

    # Automatické generovanie reportu denne o polnoci
    async def daily_report(now=None):
        report = await generate_report(db)
        hass.states.async_set(f"{DOMAIN}.daily_report", report)

    async_track_time_interval(hass, daily_report, timedelta(days=1))

    return True


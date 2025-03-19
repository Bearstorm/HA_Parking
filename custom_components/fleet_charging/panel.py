import asyncio
import json
import logging
from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .database import FleetDatabase

_LOGGER = logging.getLogger(__name__)

DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Nastavenie vlastného API pre Fleet Charging Manager."""

    db = FleetDatabase(hass)
    await db.initialize()

    async def handle_get_data(request):
        """API endpoint na získanie údajov pre vizualizáciu."""
        try:
            users = await db.get_all_users()
            vehicles = await db.get_all_vehicles()
            sessions = await db.get_all_sessions()

            data = {
                "users": users,
                "vehicles": vehicles,
                "sessions": sessions
            }

            return web.json_response(data)

        except Exception as e:
            _LOGGER.error(f"Chyba pri načítaní údajov z databázy: {e}")
            return web.json_response({"error": "Nepodarilo sa načítať údaje"}, status=500)

    hass.http.register_view(
        type("FleetChargingAPI", (web.View,), {"get": handle_get_data})
    )

    return True

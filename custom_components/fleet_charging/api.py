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
    """Nastavenie API pre Fleet Charging Manager."""
    db = FleetDatabase(hass)
    await db.initialize()

    async def handle_get_data(request):
        """API endpoint na získanie údajov."""
        try:
            users = await db.get_all_users()
            vehicles = await db.get_all_vehicles()
            sessions = await db.get_all_sessions()

            return web.json_response({
                "users": users,
                "vehicles": vehicles,
                "sessions": sessions
            })

        except Exception as e:
            _LOGGER.error(f"Chyba pri načítaní údajov: {e}")
            return web.json_response({"error": "Nepodarilo sa načítať údaje"}, status=500)

    async def handle_add_user(request):
        """API endpoint na pridanie používateľa."""
        try:
            data = await request.json()
            user_id = data.get("user_id")
            name = data.get("name")

            if not user_id or not name:
                return web.json_response({"error": "Chýbajú požadované údaje"}, status=400)

            await db.add_user(user_id, name)
            return web.json_response({"message": "Používateľ bol pridaný"})

        except Exception as e:
            _LOGGER.error(f"Chyba pri pridávaní používateľa: {e}")
            return web.json_response({"error": "Nepodarilo sa pridať používateľa"}, status=500)

    async def handle_add_vehicle(request):
        """API endpoint na pridanie vozidla."""
        try:
            data = await request.json()
            vehicle_id = data.get("vehicle_id")
            name = data.get("name")

            if not vehicle_id or not name:
                return web.json_response({"error": "Chýbajú požadované údaje"}, status=400)

            await db.add_vehicle(vehicle_id, name)
            return web.json_response({"message": "Vozidlo bolo pridané"})

        except Exception as e:
            _LOGGER.error(f"Chyba pri pridávaní vozidla: {e}")
            return web.json_response({"error": "Nepodarilo sa pridať vozidlo"}, status=500)

    async def handle_log_session(request):
        """API endpoint na zaznamenanie nabíjacej relácie."""
        try:
            data = await request.json()
            vehicle_id = data.get("vehicle_id")
            user_id = data.get("user_id")

            if not vehicle_id or not user_id:
                return web.json_response({"error": "Chýbajú požadované údaje"}, status=400)

            await db.log_session(vehicle_id, user_id)
            return web.json_response({"message": "Nabíjacia relácia bola zaznamenaná"})

        except Exception as e:
            _LOGGER.error(f"Chyba pri zaznamenaní relácie: {e}")
            return web.json_response({"error": "Nepodarilo sa zaznamenať reláciu"}, status=500)

    hass.http.register_view(
        type("FleetChargingAPI", (web.View,), {"get": handle_get_data})
    )
    hass.http.register_view(
        type("FleetChargingAddUserAPI", (web.View,), {"post": handle_add_user})
    )
    hass.http.register_view(
        type("FleetChargingAddVehicleAPI", (web.View,), {"post": handle_add_vehicle})
    )
    hass.http.register_view(
        type("FleetChargingLogSessionAPI", (web.View,), {"post": handle_log_session})
    )

    return True


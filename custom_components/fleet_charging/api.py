import logging
import json
from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import HomeAssistantType
from .database import FleetDatabase

_LOGGER = logging.getLogger(__name__)
DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistantType, config: dict):
    """Nastavenie API servera."""
    hass.http.register_view(FleetChargingAPI(hass))
    return True

class FleetChargingAPI(web.View):
    """API pre správu vozidiel, používateľov a wallboxov."""

    def __init__(self, hass: HomeAssistant):
        """Inicializácia API."""
        self.hass = hass
        self.db = FleetDatabase(hass)

    async def get(self, request):
        """Spracovanie GET požiadaviek."""
        try:
            action = request.query.get("action")

            if action == "get_vehicles":
                vehicles = await self.db.get_all_vehicles()
                return web.json_response({"vehicles": vehicles})

            if action == "get_users":
                users = await self.db.get_all_users()
                return web.json_response({"users": users})

            if action == "get_active_session":
                session = await self.db.get_latest_session()
                return web.json_response({"active_session": session})

            return web.json_response({"error": "Neznáma akcia"}, status=400)

        except Exception as e:
            _LOGGER.error(f"Chyba API: {e}")
            return web.json_response({"error": "Interná chyba servera"}, status=500)

    async def post(self, request):
        """Spracovanie POST požiadaviek."""
        try:
            data = await request.json()
            action = data.get("action")

            if action == "assign_vehicle":
                vehicle_id = data.get("vehicle_id")
                user_id = data.get("user_id")

                if not vehicle_id or not user_id:
                    return web.json_response({"error": "Chýbajúce parametre"}, status=400)

                await self.db.assign_vehicle_to_user(vehicle_id, user_id)
                return web.json_response({"success": True})

            if action == "authorize_wallbox":
                wallbox_id = data.get("wallbox_id")
                user_id = data.get("user_id")

                if not wallbox_id or not user_id:
                    return web.json_response({"error": "Chýbajúce parametre"}, status=400)

                await self.db.authorize_wallbox(wallbox_id, user_id)
                return web.json_response({"success": True})

            return web.json_response({"error": "Neznáma akcia"}, status=400)

        except Exception as e:
            _LOGGER.error(f"Chyba API: {e}")
            return web.json_response({"error": "Interná chyba servera"}, status=500)


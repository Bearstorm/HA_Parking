import asyncio
import json
from aiohttp import web
from homeassistant.core import HomeAssistant
from .database import FleetDatabase

DOMAIN = "fleet_charging"

async def async_setup(hass: HomeAssistant, config: dict):
    hass.http.register_view(FleetChargingAPI(hass))
    return True

class FleetChargingAPI(web.View):
    """Hlavná API trieda pre Fleet Charging Manager."""

    def __init__(self, hass):
        """Inicializácia API s odkazom na databázu."""
        self.hass = hass
        self.db = FleetDatabase(hass)

    async def get(self, request):
        """Spracovanie GET požiadavky – Načítanie zoznamu užívateľov, vozidiel, wallboxov a relácií."""
        users = await self.db.get_all_users()
        vehicles = await self.db.get_all_vehicles()
        wallboxes = await self.db.get_all_wallboxes()
        sessions = await self.db.get_all_sessions()

        return web.json_response({
            "users": users,
            "vehicles": vehicles,
            "wallboxes": wallboxes,
            "sessions": sessions
        })

    async def post(self, request):
        """Spracovanie POST požiadavky – Pridanie užívateľa, vozidla alebo nastavenie wallboxu."""
        try:
            data = await request.json()
            action = data.get("action")

            if action == "assign_vehicle":
                user_id = data["user_id"]
                vehicle_id = data["vehicle_id"]
                await self.db.assign_vehicle(user_id, vehicle_id)
                return web.json_response({"message": "Používateľ bol priradený k vozidlu."})

            elif action == "set_wallbox":
                wallbox_id = data["wallbox_id"]
                vehicle_id = data["vehicle_id"]
                await self.db.set_wallbox(vehicle_id, wallbox_id)
                return web.json_response({"message": "Wallbox bol nastavený pre vozidlo."})

            elif action == "add_user":
                user_id = data["user_id"]
                user_name = data["user_name"]
                await self.db.add_user(user_id, user_name)
                return web.json_response({"message": "Používateľ bol pridaný."})

            elif action == "add_vehicle":
                vehicle_id = data["vehicle_id"]
                vehicle_name = data["vehicle_name"]
                await self.db.add_vehicle(vehicle_id, vehicle_name)
                return web.json_response({"message": "Vozidlo bolo pridané."})

            else:
                return web.json_response({"error": "Neznáma akcia."}, status=400)

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

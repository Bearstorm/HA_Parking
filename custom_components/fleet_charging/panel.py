import logging
import json
from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)

class FleetChargingPanel(HomeAssistantView):
    """Vlastný panel pre správu Fleet Charging Manager v Home Assistant."""

    url = "/api/fleet_charging"
    name = "api:fleet_charging"
    requires_auth = True

    def __init__(self, hass):
        """Inicializácia panela."""
        self.hass = hass
        self.db = hass.data.get("fleet_charging", {}).get("db")

    async def get(self, request):
        """Spracovanie GET požiadavky na získanie údajov."""
        if not self.db:
            return self.json_message("Databáza nie je dostupná", status_code=500)

        users = await self.db.get_all_users()
        vehicles = await self.db.get_all_vehicles()
        sessions = await self.db.get_all_sessions()
        wallboxes = await self.db.get_all_wallboxes()

        return self.json({
            "users": users,
            "vehicles": vehicles,
            "sessions": sessions,
            "wallboxes": wallboxes
        })

    async def post(self, request):
        """Spracovanie POST požiadavky na úpravu údajov."""
        if not self.db:
            return self.json_message("Databáza nie je dostupná", status_code=500)

        try:
            data = await request.json()
            action = data.get("action")

            if action == "add_user":
                await self.db.add_user(data["user_id"], data["name"])
            elif action == "add_vehicle":
                await self.db.add_vehicle(data["vehicle_id"], data["name"])
            elif action == "assign_vehicle":
                await self.db.assign_vehicle_to_user(data["user_id"], data["vehicle_id"])
            elif action == "set_wallbox":
                await self.db.assign_wallbox_to_vehicle(data["wallbox_id"], data["vehicle_id"])
            else:
                return self.json_message("Neznáma akcia", status_code=400)

            return self.json_message("Údaje boli aktualizované", status_code=200)

        except Exception as e:
            _LOGGER.error("Chyba pri spracovaní požiadavky: %s", str(e))
            return self.json_message("Chyba pri aktualizácii údajov", status_code=500)

async def async_setup_panel(hass):
    """Registrácia API panela v Home Assistant."""
    hass.http.register_view(FleetChargingPanel(hass))
    _LOGGER.info("Fleet Charging panel bol úspešne načítaný")

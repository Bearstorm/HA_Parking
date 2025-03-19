import os
import logging
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class FleetChargingPanel(HomeAssistantView):
    """Vytvorenie API endpointu pre vizualizáciu v integrácii."""

    url = "/api/fleet_charging"
    name = "api:fleet_charging"
    requires_auth = True

    def __init__(self, hass: HomeAssistant):
        """Inicializácia s referenciou na Home Assistant."""
        self.hass = hass
        self.db = hass.data["fleet_charging"]["db"]

    async def get(self, request):
        """Načítanie všetkých údajov potrebných pre panel."""
        try:
            users = await self.db.get_all_users()
            vehicles = await self.db.get_all_vehicles()
            sessions = await self.db.get_all_sessions()

            return self.json({
                "users": users,
                "vehicles": vehicles,
                "sessions": sessions
            })
        except Exception as e:
            _LOGGER.error(f"Chyba pri načítaní údajov: {e}")
            return self.json({"error": "Nepodarilo sa načítať údaje"}, status=500)

async def async_setup_panel(hass: HomeAssistant):
    """Registrácia API panelu v Home Assistant."""
    hass.http.register_view(FleetChargingPanel(hass))

from homeassistant.components.panel_custom import register_panel
from homeassistant.components.frontend import async_register_built_in_panel
import json

async def async_setup(hass, config):
    """Registrácia vlastného panelu v integrácii."""
    panel_config = {
        "title": "Fleet Charging Manager",
        "icon": "mdi:ev-station",
        "js_url": "/local/fleet_charging_manager.js",
        "config": {
            "show_sidebar": True
        }
    }
    async_register_built_in_panel(hass, "iframe", "Fleet Charging", "fleet_charging", config=panel_config)
    return True

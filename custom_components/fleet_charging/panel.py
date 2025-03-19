from homeassistant.components.frontend import async_register_panel
from homeassistant.core import HomeAssistant
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "fleet_charging"

async def async_setup_entry(hass: HomeAssistant, entry):
    """Registrovanie vlastného panela v Home Assistant."""
    
    hass.http.register_static_path(
        f"/local/{DOMAIN}_panel.js",
        hass.config.path(f"custom_components/{DOMAIN}/panel.js"),
        False
    )

    async_register_panel(
        hass,
        component_name="custom",
        sidebar_title="Fleet Charging",
        sidebar_icon="mdi:ev-station",
        module_url=f"/local/{DOMAIN}_panel.js"
    )

    _LOGGER.info("Panel %s bol úspešne zaregistrovaný!", DOMAIN)
    return True


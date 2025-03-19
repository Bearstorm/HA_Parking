from homeassistant.components.panel_custom import async_register_panel
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Registrácia vlastného panelu do Home Assistant."""
    hass.http.register_static_path("/fleet_charging", hass.config.path("custom_components/fleet_charging/www"), False)
    async_register_panel(
        hass,
        frontend_url_path="fleet_charging",
        module_url="/fleet_charging/panel.js",
        sidebar_title="Fleet Charging",
        sidebar_icon="mdi:ev-station",
        require_admin=True
    )
    return True

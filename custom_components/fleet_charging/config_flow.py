import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from .database import FleetDatabase

class ConfigFlow(config_entries.ConfigFlow, domain="fleet_charging"):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            db = FleetDatabase(self.hass)
            await db.initialize()
            vehicle_id = user_input["vehicle_id"]
            vehicle_name = user_input["vehicle_name"]
            user_id = user_input["user_id"]
            user_name = user_input["user_name"]

            await db.add_vehicle(vehicle_id, vehicle_name)
            await db.add_user(user_id, user_name=user_input["user_name"])

            return self.async_create_entry(title="Fleet Charging", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("vehicle_id"): str,
                vol.Required("vehicle_name"): str,
                vol.Required("user_id"): str,
                vol.Required("user_name"): str,
            }),
            errors=errors
        )


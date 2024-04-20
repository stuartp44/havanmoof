"""Config flow for Moof integration."""
import voluptuous as vol
from homeassistant import config_entries
from pymoof.tools import retrieve_bikes
import asyncio

class VanMoofFlowHandler(config_entries.ConfigFlow, domain="vanmoof"):
    """Handle a Moof config flow."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            username = user_input.get("username")
            password = user_input.get("password")

            bikes = await asyncio.to_thread(retrieve_bikes.query, username, password)

            if bikes:
                return self.async_create_entry(title="VanMoof Bike Integration", data={"username": username, "password": password})
            else:
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "Unable to retrieve bikes or no bikes exist in your account. Please check your credentials and try again. "},
                    data_schema=vol.Schema({
                        vol.Required("username"): str,
                        vol.Required("password"): str,
                    }),
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            }),
        )

config_entries.HANDLERS.register(VanMoofFlowHandler)
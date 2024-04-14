"""Config flow for Moof integration."""
import voluptuous as vol
from homeassistant import config_entries, core
from pymoof.tools import retrieve_encryption_key
from homeassistant.helpers import async_add_executor_job

class VanMoofFlowHandler(config_entries.ConfigFlow, domain="vanmoof"):
    """Handle a Moof config flow."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Validate the user input here if needed
            username = user_input.get("username")
            password = user_input.get("password")

            # Retrieve encryption key
            key = await async_add_executor_job(retrieve_encryption_key.query, username, password)

            if key:
                # List bikes
                bikes = []

                if bikes:
                    # Successfully retrieved bikes, create entry
                    return self.async_create_entry(title="Moof Integration", data=user_input)
                else:
                    # Unable to retrieve bikes
                    return self.async_show_form(
                        step_id="user",
                        errors={"base": "Unable to retrieve bikes. Please check your credentials and try again."},
                        data_schema=vol.Schema({
                            vol.Required("username"): str,
                            vol.Required("password"): str,
                        }),
                    )
            else:
                # Unable to retrieve encryption key
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "Unable to retrieve encryption key. Please check your credentials and try again."},
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
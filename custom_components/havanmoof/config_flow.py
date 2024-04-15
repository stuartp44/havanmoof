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
            # Validate the user input here if needed
            username = user_input.get("username")
            password = user_input.get("password")

            # Retrieve encryption key
            bikes = await asyncio.to_thread(retrieve_bikes.query, username, password)

            if bikes:
                for bike in bikes:
                    encryption_key = bike["key"]["encryptionKey"]
                    user_key_id = bike["key"]["userKeyId"]
                    frameNumber = bike["key"]["frameNumber"]
                    uuid = bike["key"]["macAddress"].replace(":", "").lower(),

                    bike_data = {
                        "encryption_key": encryption_key,
                        "user_key_id": user_key_id,
                        "frameNumber": frameNumber,
                        "uuid": uuid
                    }
                    
                # Create entry for the bike
                return self.async_create_entry(title="Moof Integration", data=bike_data)
            else:
                # Unable to retrieve encryption key
                return self.async_show_form(
                    step_id="user",
                    errors={"base": "Unable to retrieve bikes. Please check your credentials and try again."},
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
"""VanMoof Home Assistant"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import bluetooth_tracker
import logging

DOMAIN = "havanmoof"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    """Setting up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        _LOGGER.info("Starting up VanMoof integration")
    await log_devices_with_uuids(hass)
    # Perform any additional setup here
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Perform any additional cleanup here
    return True

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Remove a config entry."""
    # Perform any additional cleanup here
    return True

async def log_devices_with_uuids(hass):
    """Scan for devices advertising specified UUIDs and log their information."""
    try:
        # Get Bluetooth devices tracked by Home Assistant
        devices = bluetooth_tracker.async_get_tracker(hass).async_see()

        for device in devices:
            # Check if any of the specified UUIDs are in the device's UUIDs
            if any(uuid in device['uuid'] for uuid in [
                "6acc5540-e631-4069-944d-b8ca7598ad50",
                "8e7f1a50-087a-44c9-b292-a2c628fdd9aa",
                "6acb5520-e631-4069-944d-b8ca7598ad50",
            ]):
                _LOGGER.info(f"Found device: {device}")
    except Exception as e:
        _LOGGER.error(f"Error scanning for devices: {e}")
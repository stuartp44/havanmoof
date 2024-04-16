"""VanMoof Home Assistant"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import bluetooth
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
    await process_discovered_service_info(hass)
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

async def process_discovered_service_info(hass):
    """Process discovered Bluetooth service info."""
    try:
        service_info_dict = await bluetooth.async_discovered_service_info(hass, connectable=True)
        service_infos = list(service_info_dict.values())  # Convert dict_values to list
        for service_info in service_infos:
            _LOGGER.info("Discovered service info: %s", service_info)
    except Exception as e:
        _LOGGER.error("Error processing discovered service info: %s", e)
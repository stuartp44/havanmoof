"""VanMoof Home Assistant"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import bluetooth
import logging

DOMAIN = "havanmoof"
_LOGGER = logging.getLogger(__name__)

# Define the VanMoof UUIDs
vanmoof_bike_uuids = {
    "SX3":"6acc5540-e631-4069-944d-b8ca7598ad50",
    "SX1/SX2":"8e7f1a50-087a-44c9-b292-a2c628fdd9aa",
    "SX1":"6acb5520-e631-4069-944d-b8ca7598ad50",
}

async def async_setup(hass: HomeAssistant, config: ConfigEntry):
    """Setting up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        _LOGGER.info("Starting up VanMoof integration")
    await process_discovered_service_info(hass, vanmoof_bike_uuids)
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
        await hass.async_add_executor_job(process_discovered_service_info_in_executor, hass, vanmoof_bike_uuids)
    except Exception as e:
        _LOGGER.error("Error processing discovered service info: %s", e)

def process_discovered_service_info_in_executor(hass, vanmoof_bike_uuids):
    """Process discovered Bluetooth service info in a separate thread."""
    try:
        service_infos = hass.components.bluetooth.async_discovered_service_info(hass, connectable=True)
        for service_info in service_infos:
            # Check if any of the service UUIDs are in the VanMoof UUIDs map
            for model, uuid in vanmoof_bike_uuids.items():
                if uuid in service_info.service_uuids:
                    _LOGGER.info("Discovered VanMoof Bike: Model=%s, UUIDs=%s, Address=%s, RSSI=%s",
                                model, service_info.service_uuids, service_info.address, service_info.rssi)
    except Exception as e:
        _LOGGER.error("Error processing discovered service info: %s", e)
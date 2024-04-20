"""VanMoof Bike Home Assistant"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import async_add_entities
from pymoof.tools import retrieve_bikes
from .binary_sensor import BikePresenceBinarySensor
from .sensor import BikeBatterySensor
import logging

DOMAIN = "havanmoof"
_LOGGER = logging.getLogger(__name__)

# Define the VanMoof UUIDs
vanmoof_bikes_uuids = {
    "SX3":"6acc5540-e631-4069-944d-b8ca7598ad50",
    "SX1/SX2":"8e7f1a50-087a-44c9-b292-a2c628fdd9aa",
    "SX1":"6acb5520-e631-4069-944d-b8ca7598ad50",
}

async def async_setup(hass: HomeAssistant, config: ConfigEntry):                            
    """Setting up this integration using YAML is not supported."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    username = entry.data.get('username')
    password = entry.data.get('password')
    bikes = await hass.async_add_executor_job(retrieve_bikes.query, username, password)
    
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        _LOGGER.info("Starting up VanMoof integration")

    # Create binary sensors for presence detection
    binary_sensors = []
    for bike in bikes:
        binary_sensors.append(BikePresenceBinarySensor(hass, bike))
    async_add_entities(binary_sensors)
    
    sensors = []
    for bike in bikes:
        sensors.append(BikeBatterySensor(hass, bike))
    async_add_entities(sensors)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Perform any additional cleanup here
    return True

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Remove a config entry."""
    # Perform any additional cleanup here
    return True

async def discover_bikes(hass):
    """Process discovered Bluetooth service info."""
    try:
        await hass.async_add_executor_job(discover_bikes_executor, hass, vanmoof_bikes_uuids)
    except Exception as e:
        _LOGGER.error("Error processing discovered service info: %s", e)

def discover_bikes_executor(hass, vanmoof_bikes_uuids):
    """Process discovered Bluetooth service info in a separate thread."""
    try:
        service_infos = hass.components.bluetooth.async_discovered_service_info(hass, connectable=True)
        for service_info in service_infos:
            # Check if any of the service UUIDs are in the VanMoof UUIDs map
            for model, uuid in vanmoof_bikes_uuids.items():
                if uuid in service_info.service_uuids:
                    _LOGGER.info("Discovered VanMoof Bike: Model=%s, UUIDs=%s, Address=%s, RSSI=%s",
                                model, service_info.service_uuids, service_info.address, service_info.rssi)
    except Exception as e:
        _LOGGER.error("Error processing discovered service info: %s", e)
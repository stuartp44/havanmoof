import logging

from pymoof.tools import retrieve_bikes, discover_bike

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up the Vanmoof sensors from a config entry."""

    # Get bikes from the Vanmoof API
    try:
        bikes = await hass.async_add_executor_job(
            retrieve_bikes.query, entry.data["username"], entry.data["password"]
        )
    except Exception as e:
        _LOGGER.error("Error setting up Vanmoof platform for sensor: %s", e)
        return False

    # If we get bikes, add the sensors
    if bikes:
        _LOGGER.info("Found %s bikes on VanMoof API", len(bikes))
        sensors = []
        for bike in bikes:
            sensors.append(VanmoofBatterySensor(bike, entry))
            sensors.append(VanmoofPresenceSensor(bike, entry))

        async_add_entities(sensors)
    else:
        _LOGGER.info("No bikes found on VanMoof API")

    # Get all advertised bikes using bluetooth
    try:
        bluetooth_discovered_bikes = await check_and_discover_bikes(hass)
    except Exception as e:
        _LOGGER.error("Error setting up Vanmoof platform for sensor: %s", e)
        bluetooth_discovered_bikes = []

    if bluetooth_discovered_bikes:
        _LOGGER.info("Found %s bikes using bluetooth", len(bluetooth_discovered_bikes))
    else:
        _LOGGER.info("No bikes found using bluetooth")

async def check_and_discover_bikes(hass):
    """Check and discover bikes using Bluetooth."""
    scanner = bluetooth.async_get_scanner(hass)
    discovered_bikes = await discover_bike.query(scanner)
    return discovered_bikes

class VanmoofBatterySensor(Entity):
    def __init__(self, bike, entry):
        self._bike = bike
        self._entry = entry
        self._attr_name = f"{bike['name']} Battery"
        self._attr_unique_id = f"{bike['id']}_battery"
        self._attr_unit_of_measurement = "%"
        self._attr_device_class = "battery"

    @property
    def state(self):
        return "100"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._bike["id"])},
            "name": self._bike["name"],
            "manufacturer": "VanMoof",
            "model": self._bike["modelDetails"]["Edition"],
            "sw_version": self._bike["smartmoduleCurrentVersion"],
            "serial_number": self._bike["frameNumber"],
        }


class VanmoofPresenceSensor(Entity):
    def __init__(self, bike, entry):
        self._bike = bike
        self._entry = entry
        self._attr_name = f"{bike['name']} Presence"
        self._attr_unique_id = f"{bike['id']}_presence"
        self._attr_device_class = "presence"

    @property
    def state(self):
        return True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._bike["id"])},
            "name": self._bike["name"],
            "manufacturer": "VanMoof",
            "model": self._bike["modelDetails"]["Edition"],
            "sw_version": self._bike["smartmoduleCurrentVersion"],
            "serial_number": self._bike["frameNumber"],
        }

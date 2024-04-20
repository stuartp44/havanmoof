"""Platform for typical sensor integration."""
from homeassistant.helpers.entity import Entity
from .const import DOMAIN
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

class BikeBatterySensor(Entity):
    def __init__(self, hass, bike_data):
        self._hass = hass
        self._bike_data = bike_data

    @property
    def name(self):
        return f"{self._bike_data['name']} Battery Level"

    @property
    def unique_id(self):
        return f"{self._bike_data['id']}_battery"

    @property
    def state(self):
        return self._bike_data.get('battery_level')

    @property
    def unit_of_measurement(self):
        return "%"

    async def async_update(self):
        pass
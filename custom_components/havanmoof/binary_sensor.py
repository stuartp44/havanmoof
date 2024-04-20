"""Platform for binary sensor integration."""
from homeassistant.helpers.entity import Entity

class BikePresenceBinarySensor(Entity):
    def __init__(self, hass, bike_data):
        self._hass = hass
        self._bike_data = bike_data
        self._is_present = False

    @property
    def name(self):
        return f"{self._bike_data['name']} Presence"

    @property
    def unique_id(self):
        return f"{self._bike_data['id']}_presence"

    @property
    def state(self):
        return "Present" if self._is_present else "Not Present"

    async def async_update(self):
        # Check presence via Bluetooth advertisements
        bluetooth_devices = self._hass.states.async_entity_ids('device_tracker')
        bike_mac_address = self._bike_data['mac_address']

        for device in bluetooth_devices:
            device_state = self._hass.states.get(device)
            if device_state.attributes.get('mac') == bike_mac_address:
                self._is_present = True
                return

        self._is_present = False
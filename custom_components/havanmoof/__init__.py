"""VanMoof Bike Home Assistant"""
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pymoof.tools import retrieve_bikes
from homeassistant.const import (
    Platform,
)
import logging
from .const import DOMAIN, CONF_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = VanMoofCoordinator(hass, entry)

    await coordinator.async_refresh()
    
    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    if hass.data.get(DOMAIN) is None:
        _LOGGER.info("Starting up VanMoof integration")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Perform any additional cleanup here
    return True

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Remove a config entry."""
    # Perform any additional cleanup here
    return True
        
class VanMoofCoordinator(DataUpdateCoordinator):
    """Data update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(
                minutes=CONF_SCAN_INTERVAL
            ),
            username=entry.data.get("username"),
            password=entry.data.get("password"),
        )
        self._entry = entry


    @property
    def entry_id(self) -> str:
        """Return entry ID."""
        return self._entry.entry_id
    
    # define username and password as properties
    @property
    def username(self) -> str:
        """Return username."""
        return self._entry.data.get("username")
    
    @property
    def password(self) -> str:
        """Return password."""
        return self._entry.data.get("password")
    

    async def _async_get_bikes(self) -> dict:
        """Fetch the latest data from the source."""
        bikes = await self.hass.async_add_executor_job(retrieve_bikes.query, self.username, self.password)
        return bikes
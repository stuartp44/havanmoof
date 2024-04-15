"""VanMoof Home Assistant"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_setup(
    hass: HomeAssistant, config: Config
):  # pylint: disable=unused-argument;
    """Setting up this integration using YAML is not supported."""
    return True
"""The Itho RFT Remote component."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, Platform
from homeassistant.core import HomeAssistant

from .itho_remote import IthoRemoteRFT
from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    itho_remote = IthoRemoteRFT(port=entry.data[CONF_PORT])
    hass.data[DOMAIN] = {"itho_remote": itho_remote}

    itho_remote.start()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry
        # config_entry, PLATFORMS
    )
    if unload_ok:
        itho_remote = hass.data[DOMAIN]
        itho_remote.stop()
    return unload_ok

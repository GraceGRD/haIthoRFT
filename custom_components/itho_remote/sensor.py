"""Support for Itho Remote sensors."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import Event, HomeAssistant, callback

from .itho_remote import IthoRemoteRFT
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Itho Remote sensors."""
    itho_remote = hass.data[DOMAIN]["itho_remote"]

    version = str(itho_remote.version())

    sensor = IthoRemoteVersionSensor(version)
    async_add_entities([sensor])

    return True


class IthoRemoteVersionSensor(Entity):
    def __init__(self, version):
        self._version = version

    @property
    def name(self):
        return "Itho Remote Version"

    @property
    def state(self):
        return self._version

    @property
    def unique_id(self):
        return "itho_remote_version"

    @property
    def icon(self):
        return "mdi:information-outline"

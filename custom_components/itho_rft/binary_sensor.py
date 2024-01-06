"""Support for Itho binary sensor."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import IthoCoordinator
from .models import IthoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Itho binary sensor based on a config entry."""
    coordinator: IthoCoordinator = hass.data[DOMAIN][entry.entry_id]

    binary_sensors = [
        FlagsFaultActiveBinarySensor(coordinator),
        FlagsFilterDirtyBinarySensor(coordinator),
    ]
    async_add_entities(binary_sensors)

    return True


class FlagsFaultActiveBinarySensor(IthoEntity, BinarySensorEntity):
    """Defines a Itho flags fault active binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_name = "Internal fault"

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "_fault"

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        flags = self.coordinator.remote.data.get("flags")
        if flags is not None:
            fault_active = flags.get("fault_active")
            if fault_active is not None:
                return bool(fault_active)

        return False  # TODO: What if None?


class FlagsFilterDirtyBinarySensor(IthoEntity, BinarySensorEntity):
    """Defines a Itho flags filter dirty binary sensor."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_name = "Filter Dirty"

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "_filter_dirty"

    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        flags = self.coordinator.remote.data.get("flags")
        if flags is not None:
            filter_dirty = flags.get("filter_dirty")
            if filter_dirty is not None:
                return bool(filter_dirty)

        return False  # TODO: What if None?

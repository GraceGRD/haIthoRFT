"""Models for Itho."""

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, BRAND, MODEL
from .coordinator import IthoCoordinator


class IthoEntity(CoordinatorEntity[IthoCoordinator]):
    """Defines a base Itho entity."""

    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this WLED device."""
        return DeviceInfo(
            identifiers={
                (DOMAIN, self.coordinator.remote.remote_address)
                },
            name=NAME,
            manufacturer=BRAND,
            model=MODEL
        )

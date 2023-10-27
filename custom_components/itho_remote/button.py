"""Support for Itho button."""
from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import IthoCoordinator
from .models import IthoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Itho button based on a config entry."""
    coordinator: IthoCoordinator = hass.data[DOMAIN][entry.entry_id]

    # TODO: Change command: any to enum and get available buttons from IthoRFT class?
    buttons = [
        RemotePairButton(coordinator),
        RemoteCommandButton(coordinator, "auto"),
        RemoteCommandButton(coordinator, "low"),
        RemoteCommandButton(coordinator, "high"),
        RemoteCommandButton(coordinator, "timer10"),
        RemoteCommandButton(coordinator, "timer20"),
        RemoteCommandButton(coordinator, "timer30"),
        RemoteRequestDataButton(coordinator),
    ]
    async_add_entities(buttons)

    return True


class RemoteCommandButton(IthoEntity, ButtonEntity):
    """Defines a Itho remote button."""

    # _attr_device_class = ButtonDeviceClass. # TODO: what class?
    # _attr_entity_category = EntityCategory. # TODO: what category?

    def __init__(self, coordinator: IthoCoordinator, command) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator
        self.command = command

        self._attr_unique_id = f"_{self.command}"
        self._attr_name = self.command.capitalize()

    def press(self) -> None:
        """Press the button to send the associated command."""
        return self.coordinator.remote.command(self.command)


class RemotePairButton(IthoEntity, ButtonEntity):
    """Defines a Itho remote button."""

    # _attr_device_class = ButtonDeviceClass. # TODO: what class?
    # _attr_entity_category = EntityCategory. # TODO: what category?

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator

        self._attr_unique_id = "_pair"
        self._attr_name = "Pair"

    def press(self) -> None:
        """Press the button to initiate the pairing process."""
        return self.coordinator.remote.pair()


class RemoteRequestDataButton(IthoEntity, ButtonEntity):
    """Defines a Itho request data button."""

    _attr_device_class = ButtonDeviceClass.UPDATE  # TODO: what class?
    # _attr_entity_category = EntityCategory. # TODO: what category?

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator=coordinator)
        self.coordinator = coordinator

        self._attr_unique_id = "_request_data"
        self._attr_name = "Request Data"

    def press(self) -> None:
        """Press the button to request data."""
        return self.coordinator.remote.request_data()

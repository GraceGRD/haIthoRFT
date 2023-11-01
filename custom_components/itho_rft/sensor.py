"""Support for Itho sensors."""
from __future__ import annotations

from decimal import Decimal

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import IthoCoordinator
from .models import IthoEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Itho sensor based on a config entry."""
    coordinator: IthoCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        IthoRemoteAddressSensorEntity(coordinator),
        IthoUnitAddressSensorEntity(coordinator),
        IthoStateSensorEntity(coordinator),
        IthoCo2SensorEntity(coordinator),
        IthoBypassValveSensorEntity(coordinator),
        IthoTimeRemainingSensorEntity(coordinator),
        IthoTemperatureSensorEntity(coordinator, "exhaust_temperature"),
        IthoTemperatureSensorEntity(coordinator, "supply_temperature"),
        IthoTemperatureSensorEntity(coordinator, "indoor_temperature"),
        IthoTemperatureSensorEntity(coordinator, "outdoor_temperature"),
        IthoFlowSensorEntity(coordinator, "inlet_flow"),
        IthoFlowSensorEntity(coordinator, "exhaust_flow"),
    ]
    async_add_entities(sensors)

    return True


class IthoRemoteAddressSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho remote address sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the remote address sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = "remote_address"
        self._attr_name = "Remote Address"
        self._attr_icon = "mdi:remote"

    @property
    def native_value(self) -> StateType | str:
        """Get the native value of the sensor."""
        return self.coordinator.remote.remote_address


class IthoUnitAddressSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho unit address sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the unit address sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = "unit_address"
        self._attr_name = "Unit Address"
        self._attr_icon = "mdi:hvac"

    @property
    def native_value(self) -> StateType | str:
        """Get the native value of the sensor."""
        return self.coordinator.remote.unit_address


class IthoStateSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho state sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the temperature sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "state"
        self._attr_name = "State"
        self._attr_icon = "mdi:thermostat-box-auto"
        self._attr_device_class = SensorDeviceClass.ENUM

    @property
    def native_value(self) -> StateType:
        """Get the native value of the sensor."""
        flags = self.coordinator.remote.data.get("flags")
        if flags is not None:
            active_speed_mode = flags.get("active_speed_mode")
            if active_speed_mode is not None:
                return active_speed_mode

        return None  # TODO: What if None?


class IthoCo2SensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho co2 sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the co2 sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "co2"
        self._attr_name = "Co2"
        self._attr_icon = "mdi:molecule-co2"
        self._attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION
        self._attr_device_class = SensorDeviceClass.CO2
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Get the native value of the sensor."""
        return self.coordinator.remote.data.get("co2_level")  # TODO: What if None?


class IthoBypassValveSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho bypass valve sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the bypass valve sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "bypass_valve"
        self._attr_name = "Bypass valve"
        self._attr_icon = "mdi:valve"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType:
        """Get the native value of the sensor."""
        return self.coordinator.remote.data.get(
            "bypass_position"
        )  # TODO: What if None?


class IthoTimeRemainingSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho time remaining sensor entity."""

    def __init__(self, coordinator: IthoCoordinator) -> None:
        """Initialize the time remaining sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = "time_remaining"
        self._attr_name = "Time remaining"
        self._attr_icon = "mdi:timer-outline"
        self._attr_native_unit_of_measurement = UnitOfTime.MINUTES
        self._attr_device_class = SensorDeviceClass.DURATION
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType | Decimal:
        """Get the native value of the sensor."""
        return self.coordinator.remote.data.get("remaining_time")  # TODO: What if None?


class IthoTemperatureSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho temperature sensor entity."""

    def __init__(self, coordinator: IthoCoordinator, sensor_id: str) -> None:
        """Initialize the temperature sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = sensor_id
        self._attr_name = " ".join(map(str, sensor_id.capitalize().split("_")))
        self._attr_icon = "mdi:thermometer"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType | Decimal:
        """Get the native value of the sensor."""
        return self.coordinator.remote.data.get(
            self._attr_unique_id
        )  # TODO: What if None?


class IthoFlowSensorEntity(IthoEntity, SensorEntity):
    """Defines a Itho flow sensor entity."""

    def __init__(self, coordinator: IthoCoordinator, sensor_id: str) -> None:
        """Initialize the flow sensor entity."""
        super().__init__(coordinator=coordinator)
        self._attr_unique_id = sensor_id
        self._attr_name = " ".join(map(str, sensor_id.capitalize().split("_")))
        self._attr_icon = "mdi:air-filter"
        self._attr_native_unit_of_measurement = "m3/h"
        self._attr_device_class = "Flow"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> StateType | Decimal:
        """Get the native value of the sensor."""
        return self.coordinator.remote.data.get(
            self._attr_unique_id
        )  # TODO: What if None?

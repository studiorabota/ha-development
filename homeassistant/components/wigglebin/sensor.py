"""Platform for sensor integration."""

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        WiggleBinSensor(
            coordinator,
            "wigglebin_temperature",
            "WiggleBin Temperature",
            "temperature",
            SensorDeviceClass.TEMPERATURE,
        ),
        WiggleBinSensor(
            coordinator,
            "wigglebin_humidity",
            "WiggleBin Humidity",
            "humidity",
            SensorDeviceClass.HUMIDITY,
        ),
        # Add more sensors as needed
    ]

    async_add_entities(sensors, True)


class WiggleBinSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self, coordinator, sensor_id, name, attribute, device_class: SensorDeviceClass
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_id = sensor_id
        self._name = name
        self._attribute = attribute
        self._device_class = device_class

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get("environment", {}).get(self._attribute)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return self.coordinator.data

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._sensor_id

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        return self.coordinator.last_update_success

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self) -> SensorStateClass:
        """Return the state class of the sensor."""
        return SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Update the sensor."""
        await self.coordinator.async_request_refresh()

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
            f"{entry.entry_id}_temperature",
            f"{entry.title} Temperature",
            "environment",
            "temperature",
            SensorDeviceClass.TEMPERATURE,
            "°C",
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_humidity",
            f"{entry.title} Humidity",
            "environment",
            "humidity",
            SensorDeviceClass.HUMIDITY,
            "%",
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_pressure",
            f"{entry.title} Pressure",
            "environment",
            "pressure",
            SensorDeviceClass.PRESSURE,
            "hPa",
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_soil_temperature",
            f"{entry.title} Soil Temperature",
            "soil",
            "temperature",
            SensorDeviceClass.TEMPERATURE,
            "°C",
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_soil_adc",
            f"{entry.title} Soil ADC",
            "soil_moisture",
            "adc",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_image_mean_gray",
            f"{entry.title} Image Mean Gray",
            "image",
            "mean_gray",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_image_pixels_darker",
            f"{entry.title} Image Pixels Shifted To Dark",
            "image",
            "count_pixels_darker",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_image_pixels_lighter",
            f"{entry.title} Image Pixels Shifted To Light",
            "image",
            "count_pixels_darker",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_worm_count",
            f"{entry.title} Worm Count",
            "image",
            "worm_count",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_fly_count",
            f"{entry.title} Fly Count",
            "image",
            "detection_class_fly_count",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_fly_larva_count",
            f"{entry.title} Fly Larva Count",
            "image",
            "detection_class_fly_larva_count",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_detection_confidence_avg",
            f"{entry.title} Detection Confidence Average",
            "image",
            "detection_confidence_avg",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_detection_confidence_min",
            f"{entry.title} Detection Confidence Min",
            "image",
            "detection_confidence_min",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_detection_confidence_max",
            f"{entry.title} Detection Confidence Max",
            "image",
            "detection_confidence_max",
            None,
            None,
        ),
        WiggleBinSensor(
            coordinator,
            f"{entry.entry_id}_detection_count",
            f"{entry.title} Detection Count",
            "image",
            "detection_count",
            None,
            None,
        ),
    ]

    async_add_entities(sensors, True)


class WiggleBinSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(
        self,
        coordinator,
        sensor_id,
        name,
        group,
        attribute,
        device_class: SensorDeviceClass | None,
        unit_of_measurement: str | None,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._sensor_id = sensor_id
        self._name = name
        self._group = group
        self._attribute = attribute
        self._device_class = device_class
        self._unit_of_measurement = unit_of_measurement

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._group, {}).get(self._attribute)

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
    def device_class(self) -> SensorDeviceClass | None:
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self) -> SensorStateClass:
        """Return the state class of the sensor."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement

    async def async_update(self) -> None:
        """Update the sensor."""
        await self.coordinator.async_request_refresh()

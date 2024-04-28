"""Platform for typical sensor integration."""
from homeassistant.helpers.entity import Entity
from dataclasses import dataclass
from .const import DOMAIN
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

@dataclass
class VanMoofEntityDescription(SensorEntityDescription):
    """Provide a description of a Polar sensor."""

    key_category: str | None = None
    unique_id: str | None = None
    attributes_keys: list[str] | None = None

SENSORS = (
    VanMoofEntityDescription(
        key_category=ATTR_USER_DATA,
        key="weight",
        name="Weight",
        unique_id="weight",
        native_unit_of_measurement="kg",
        device_class=SensorDeviceClass.WEIGHT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Polar sensor platform."""
    coordinator: PolarCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(BikeBatterySensor(coordinator, description) for description in SENSORS)

class BikeBatterySensor(CoordinatorEntity[PolarCoordinator], SensorEntity):
    """Implementation of the Polar sensor."""

    entity_description: PolarEntityDescription
    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PolarCoordinator,
        description: PolarEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_device_info = DeviceInfo(
            configuration_url="https://flow.polar.com/",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.entry_id)},
            manufacturer="Polar",
            name=coordinator.user_name,
        )
        self._attr_unique_id = (
            f"{coordinator.entry_id}_{description.unique_id or description.key}"
        )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""

        return (
            super().available
            and self.entity_description.key
            in self.coordinator.data[self.entity_description.key_category]
        )

    @property
    def native_value(self) -> float | None:
        """Return sensor state."""
        if (
            value := self.coordinator.data[self.entity_description.key_category][
                self.entity_description.key
            ]
        ) is None:
            return None
        return value

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return attributes."""
        if self.entity_description.attributes_keys:
            attributes = {}
            for key in self.entity_description.attributes_keys:
                if key in self.coordinator.data[self.entity_description.key_category]:
                    value = self.coordinator.data[self.entity_description.key_category][
                        key
                    ]
                    attributes.update({key: value})
            return attributes
        return None

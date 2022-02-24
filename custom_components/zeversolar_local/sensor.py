"""Sensor platform for ZeverSolar inverter."""
import async_timeout
from homeassistant.components.sensor import (  # STATE_CLASS_TOTAL_INCREASING,
    STATE_CLASS_MEASUREMENT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR, POWER_WATT
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from zeversolarlocal import ZeverError, ZeverTimeout

from .const import CONF_SERIAL_NO, DOMAIN, SENSOR_CURRENT_POWER, SENSOR_DAILY_ENERGY
from .coordinator import ZeversolarApiCoordinator

# not needed
# SCAN_INTERVAL = timedelta(seconds=30)

PARALLEL_UPDATES = 1


# see: https://developers.home-assistant.io/docs/integration_fetching_data/
async def async_setup_entry(hass, entry, async_add_entities):
    """Setup sensor platform."""
    zever_coordinator: ZeversolarApiCoordinator = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(10):
                return await zever_coordinator.api.async_get_data()
        except ZeverTimeout as err:
            raise UpdateFailed(f"Timeout communicating with API: {err}") from err
        except ZeverError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    zever_coordinator.update_method = async_update_data

    await zever_coordinator.async_config_entry_first_refresh()

    serial_number = entry.data[CONF_SERIAL_NO]

    inverter = Inverter(serial_number)

    daily_energy_sensor = Sensor(SENSOR_DAILY_ENERGY)
    current_power_sensor = Sensor(SENSOR_CURRENT_POWER)

    all_sensors = (daily_energy_sensor, current_power_sensor)

    device_info = DeviceInfo(
        identifiers={(DOMAIN, inverter.serial_number)},
        name=f"ZeverSolar inverter '{inverter.serial_number}'",
        # model="Model A [model]",
        manufacturer="ZeverSolar",
        # hw_version="M10",
        # sw_version="17717-709R+17511-707R",
    )

    entities = []

    # Individual inverter sensors entities
    entities.extend(
        ZeverSolarSensor(zever_coordinator, device_info, inverter, sensor)
        for sensor in all_sensors
    )

    async_add_entities(entities)


_SENSOR_DESCRIPTIONS = {
    "current_power": SensorEntityDescription(
        key="W",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
        name="Current Power",
        icon="mdi:solar-power",
        entity_category=None,
    ),
    "daily_energy": SensorEntityDescription(
        key="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
        name="Total Energy Today",
        icon="mdi:solar-power",
        entity_category=None,
    ),
}

_DEFAULT_SENSOR = SensorEntityDescription(
    key="_",
    state_class=STATE_CLASS_MEASUREMENT,
    entity_category=EntityCategory.DIAGNOSTIC,
)


class Sensor:
    """Defines a sensor of the ZeverSolar inverter"""

    def __init__(self, sensor_id: str) -> None:
        self._sensor_id = sensor_id

    @property
    def sensor_id(self) -> str:
        """The ZeverSolar sensor ID."""
        return self._sensor_id


class Inverter:
    """Defines a ZeverSolar inverter."""

    def __init__(
        self,
        serial_number: str,
    ) -> None:
        self._serial_number = serial_number

    @property
    def serial_number(self) -> str:
        """Gets the serial number."""
        return self._serial_number


class ZeverSolarSensor(CoordinatorEntity, SensorEntity):
    """Entity representing individual inverter sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_info: DeviceInfo,
        inverter: Inverter,
        sensor: Sensor,
    ) -> None:
        """Initialize an inverter sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{DOMAIN}_{inverter.serial_number}_{sensor.sensor_id}"
        self._attr_device_info = device_info
        self.entity_description = _SENSOR_DESCRIPTIONS.get(
            sensor.sensor_id, _DEFAULT_SENSOR
        )
        self._sensor = sensor
        self._previous_value = None

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        my_data = self.coordinator.data
        if my_data is None:
            raise ConfigEntryNotReady

        value = getattr(my_data, self._sensor.sensor_id)
        self._previous_value = value
        return value

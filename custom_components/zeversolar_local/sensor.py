"""Sensor platform for Zeversolar inverter."""
import async_timeout
from homeassistant.components.sensor import (  # STATE_CLASS_TOTAL_INCREASING,
    STATE_CLASS_MEASUREMENT,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import CONF_HOST
from homeassistant.const import ENERGY_KILO_WATT_HOUR, POWER_WATT
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from zever_local.inverter import ArrayPosition, ZeversolarError, ZeversolarTimeout

from .const import CONF_SERIAL_NO, DOMAIN
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
        except ZeversolarTimeout as err:
            raise UpdateFailed(f"Timeout communicating with API: {err}") from err
        except ZeversolarError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    zever_coordinator.update_method = async_update_data

    await zever_coordinator.async_config_entry_first_refresh()

    serial_number = entry.data[CONF_SERIAL_NO]
    url = entry.data[CONF_HOST]

    inverter_data = await zever_coordinator.api.async_get_data()
    hardware_version = inverter_data.hardware_version
    software_version = inverter_data.software_version

    inverter = Inverter(serial_number, url, hardware_version, software_version)

    daily_energy_sensor = Sensor(ArrayPosition.energy_today_KWh.name)
    current_power_sensor = Sensor(ArrayPosition.pac_watt.name)

    all_sensors = (daily_energy_sensor, current_power_sensor)

    device_info = DeviceInfo(
        configuration_url=f"http://{inverter.address}",
        # default_manufacturer: str
        # default_model: str
        # default_name: str
        # entry_type: DeviceEntryType | None
        identifiers={(DOMAIN, inverter.serial_number)},
        manufacturer="Zeversolar",
        # model: str | None
        name=f"Zeversolar inverter '{inverter.serial_number}'",
        # suggested_area: str | None
        sw_version=inverter.software_version,
        hw_version=inverter.hardware_version
        # via_device: tuple[str, str]
    )

    entities = []

    # Individual inverter sensors entities
    entities.extend(
        ZeverSolarSensor(zever_coordinator, device_info, inverter, sensor)
        for sensor in all_sensors
    )

    async_add_entities(entities)


_SENSOR_DESCRIPTIONS = {
    ArrayPosition.pac_watt.name: SensorEntityDescription(
        key="W",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=POWER_WATT,
        name="Current Power",
        icon="mdi:solar-power",
        entity_category=None,
    ),
    ArrayPosition.energy_today_KWh.name: SensorEntityDescription(
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
    """Defines a sensor of the Zeversolar inverter"""

    def __init__(self, sensor_id: str) -> None:
        self._sensor_id = sensor_id

    @property
    def sensor_id(self) -> str:
        """The Zeversolar sensor ID."""
        return self._sensor_id


class Inverter:
    """Defines a Zeversolar inverter."""

    def __init__(
        self,
        serial_number: str,
        address: str,
        hardware_version: str,
        software_version: str,
    ) -> None:
        self._serial_number = serial_number
        self._address = address
        self._hardware_version = hardware_version
        self._software_version = software_version

    @property
    def serial_number(self) -> str:
        """Gets the serial number."""
        return self._serial_number

    @property
    def address(self) -> str:
        """Gets the inverter address."""
        return self._address

    @property
    def hardware_version(self) -> str:
        """Gets the hardware version."""
        return self._hardware_version

    @property
    def software_version(self) -> str:
        """Gets the software version."""
        return self._software_version


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

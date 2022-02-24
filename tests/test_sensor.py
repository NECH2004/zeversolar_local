"""Sensor tests."""
from unittest.mock import patch

from homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import UpdateFailed
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from zeversolarlocal import ZeverError, ZeverTimeout

from custom_components.zeversolar_local.const import CONF_SERIAL_NO, DOMAIN
from custom_components.zeversolar_local.coordinator import (
    ZeverSolarApiClient,
    ZeversolarApiCoordinator,
)
from custom_components.zeversolar_local.sensor import (
    Inverter,
    Sensor,
    ZeverSolarSensor,
    async_setup_entry,
)


def async_add_entities(entities):
    """Add entities to a sensor as simuation for unit test. Helper method."""
    count = entities.__len__()
    assert count == 2


async def test_async_setup_entry(hass):
    """Tests the setup of the sensor platform."""
    host = "TEST_HOST"
    client = ZeverSolarApiClient(host)
    coordinator = ZeversolarApiCoordinator(hass, client=client)

    serial_number = "ABC"
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={CONF_HOST: "TEST_HOST", CONF_SERIAL_NO: serial_number},
    )

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    config_entry.add_to_hass(hass)

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    with patch(
        "custom_components.zeversolar_local.zeversolar_api.zs.inverter_id"
    ) as api_mock_inverter:
        api_mock_inverter.return_value = serial_number

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock_solardata:
            api_mock_solardata.return_value = "any value"

            await async_setup_entry(hass, config_entry, async_add_entities)


async def test_async_setup_entry_coordinator_update_ok(hass):
    """Tests the sensor platform with updating data."""
    host = "TEST_HOST"
    client = ZeverSolarApiClient(host)
    coordinator = ZeversolarApiCoordinator(hass, client=client)
    serial_number = "Any_Number"

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={CONF_HOST: "TEST_HOST", CONF_SERIAL_NO: serial_number},
    )

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    config_entry.add_to_hass(hass)

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    with patch(
        "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
    ) as api_mock_solardata:
        solar_data_mock = "solar_data_mock"
        api_mock_solardata.return_value = solar_data_mock

        await async_setup_entry(hass, config_entry, async_add_entities)
        my_solardata = await coordinator.update_method()
        assert my_solardata == solar_data_mock


async def test_async_setup_entry_coordinator_update_fails_with_timeout(hass):
    """Tests of the sensor platform with updating data failing."""
    with pytest.raises(UpdateFailed):
        host = "TEST_HOST"
        client = ZeverSolarApiClient(host)
        coordinator = ZeversolarApiCoordinator(hass, client=client)
        serial_number = "test"

        config_entry = MockConfigEntry(
            domain=DOMAIN,
            unique_id="my_unique_test_id",
            data={CONF_HOST: "TEST_HOST", CONF_SERIAL_NO: serial_number},
        )

        if hass.data.get(DOMAIN) is None:
            hass.data.setdefault(DOMAIN, {})

        config_entry.add_to_hass(hass)

        hass.data[DOMAIN][config_entry.entry_id] = coordinator

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock_solardata:
            solar_data_mock = "solar_data_mock"
            api_mock_solardata.return_value = solar_data_mock

            await async_setup_entry(hass, config_entry, async_add_entities)

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock_solardata_fail:
            api_mock_solardata_fail.side_effect = ZeverTimeout("Timeout happened")
            await coordinator.update_method()


async def test_async_setup_entry_coordinator_update_fails_with_error(hass):
    """Tests the sensor platform with update failing."""
    with pytest.raises(UpdateFailed):
        host = "TEST_HOST"
        client = ZeverSolarApiClient(host)
        coordinator = ZeversolarApiCoordinator(hass, client=client)
        serial_number = "145e-serxsdtr"

        config_entry = MockConfigEntry(
            domain=DOMAIN,
            unique_id="my_unique_test_id",
            data={CONF_HOST: "TEST_HOST", CONF_SERIAL_NO: serial_number},
        )

        if hass.data.get(DOMAIN) is None:
            hass.data.setdefault(DOMAIN, {})

        config_entry.add_to_hass(hass)

        hass.data[DOMAIN][config_entry.entry_id] = coordinator

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock_solardata:
            solar_data_mock = "solar_data_mock"
            api_mock_solardata.return_value = solar_data_mock

            await async_setup_entry(hass, config_entry, async_add_entities)

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock_solardata_fail:
            api_mock_solardata_fail.side_effect = ZeverError("Error happened")
            await coordinator.update_method()


async def test_Sensor_class(hass):
    """Simple test for construction and initialization."""
    sensor_id = "sensor_1"

    result_sensor = Sensor(sensor_id)
    result_sensor_id = result_sensor.sensor_id

    assert type(result_sensor) is Sensor
    assert sensor_id == result_sensor_id


async def test_Inverter_class(hass):
    """Simple test for construction and initialization."""
    serial_number = "ABC_x34"

    result_inverter = Inverter(serial_number)
    result_serial_number = result_inverter.serial_number

    assert type(result_inverter) is Inverter
    assert serial_number == result_serial_number


async def test_ZeverSolarSensor_class(hass):
    """Simple test for construction and initialization."""
    serial_number = "ABC_x34"
    inverter = Inverter(serial_number)
    sensor_id = "sensor_1"
    sensor = Sensor(sensor_id)

    device_info = DeviceInfo(
        identifiers={(DOMAIN, inverter.serial_number)},
        name=f"ZeverSolar inverter '{inverter.serial_number}'",
        manufacturer="ZeverSolar",
        hw_version="M10",
        sw_version="17717-709R+17511-707R",
    )

    api_client = ZeverSolarApiClient("TEST_HOST")
    coordinator = ZeversolarApiCoordinator(hass, api_client)
    result_sensor = ZeverSolarSensor(coordinator, device_info, inverter, sensor)

    assert type(result_sensor) is ZeverSolarSensor


async def test_ZeverSolarSensor_native_value_no_data(hass):
    """Fetch data from coordinator but data is None."""
    with pytest.raises(ConfigEntryNotReady):
        serial_number = "ABC_x34"
        inverter = Inverter(serial_number)
        sensor_id = "power"
        sensor = Sensor(sensor_id)

        device_info = DeviceInfo(
            identifiers={(DOMAIN, inverter.serial_number)},
            name=f"ZeverSolar inverter '{inverter.serial_number}'",
            manufacturer="ZeverSolar",
            hw_version="M10",
            sw_version="17717-709R+17511-707R",
        )

        api_client = ZeverSolarApiClient("TEST_HOST")
        coordinator = ZeversolarApiCoordinator(hass, api_client)

        zeversolar_sensor = ZeverSolarSensor(coordinator, device_info, inverter, sensor)

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock:
            api_mock.return_value = None
            await coordinator.async_config_entry_first_refresh()
            zeversolar_sensor.native_value


async def test_ZeverSolarSensor_native_value_data(hass):
    """Fetch data from coordinator and data can be fetched."""

    class MockClass:
        power = 1234.5

    serial_number = "ABC_x34"
    inverter = Inverter(serial_number)
    sensor_id = "power"
    sensor = Sensor(sensor_id)

    device_info = DeviceInfo(
        identifiers={(DOMAIN, inverter.serial_number)},
        name=f"ZeverSolar inverter '{inverter.serial_number}'",
        manufacturer="ZeverSolar",
        hw_version="M10",
        sw_version="17717-709R+17511-707R",
    )

    api_client = ZeverSolarApiClient("TEST_HOST")
    coordinator = ZeversolarApiCoordinator(hass, api_client)

    zeversolar_sensor = ZeverSolarSensor(coordinator, device_info, inverter, sensor)

    power_mock = MockClass()

    with patch(
        "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
    ) as api_mock:
        api_mock.return_value = power_mock
        await coordinator.async_config_entry_first_refresh()

        result_native_value = zeversolar_sensor.native_value

    assert result_native_value == power_mock.power


async def test_ZeverSolarSensor_native_value_ZeverTimeout_exception(hass):
    """Fetch data from coordinator and data can be fetched."""
    with pytest.raises(ConfigEntryNotReady):

        class MockClass:
            power = 1234.5

        serial_number = "ABC_x34"
        inverter = Inverter(serial_number)
        sensor_id = "power"
        sensor = Sensor(sensor_id)

        device_info = DeviceInfo(
            identifiers={(DOMAIN, inverter.serial_number)},
            name=f"ZeverSolar inverter '{inverter.serial_number}'",
            manufacturer="ZeverSolar",
            hw_version="M10",
            sw_version="17717-709R+17511-707R",
        )

        api_client = ZeverSolarApiClient("TEST_HOST")
        coordinator = ZeversolarApiCoordinator(hass, api_client)

        zeversolar_sensor = ZeverSolarSensor(coordinator, device_info, inverter, sensor)

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock:
            api_mock.side_effect = ZeverTimeout("uups")
            await coordinator.async_config_entry_first_refresh()

            zeversolar_sensor.native_value

"""Test the coordinator classes."""
from unittest.mock import patch

from homeassistant.helpers.update_coordinator import UpdateFailed
import pytest

from custom_components.zeversolar_local.coordinator import ZeversolarApiCoordinator
from custom_components.zeversolar_local.zeversolar_api import ZeverSolarApiClient


async def test_zeversolarApiCoordinator_constructor(hass):
    """Simple test for construction and initialization."""
    api_client = ZeverSolarApiClient("TEST_HOST")
    result_coordinator = ZeversolarApiCoordinator(hass, api_client)

    assert type(result_coordinator) is ZeversolarApiCoordinator


async def test_zeversolarApiCoordinator_async_get_data_ok(hass):
    """Tests the async_get_data method returning data from the inverter."""
    api_client = ZeverSolarApiClient("TEST_HOST")
    result_coordinator = ZeversolarApiCoordinator(hass, api_client)

    with patch(
        "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
    ) as api_mock:
        api_mock.return_value = "solar_data_mock"

        result_data = await result_coordinator._async_update_data()

    assert result_data is not None
    assert result_coordinator.last_update_success


async def test_zeversolarApiCoordinator_async_get_data_exception(hass):
    """Tests the async_get_data method returning data from the inverter."""
    with pytest.raises(UpdateFailed):
        api_client = ZeverSolarApiClient("TEST_HOST")
        result_coordinator = ZeversolarApiCoordinator(hass, api_client)

        with patch(
            "custom_components.zeversolar_local.zeversolar_api.zs.solardata"
        ) as api_mock:
            api_mock.side_effect = Exception("failure")
            await result_coordinator._async_update_data()

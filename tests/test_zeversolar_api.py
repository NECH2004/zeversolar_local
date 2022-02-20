"""Tests the ZeverSolar API wrapper."""
from custom_components.zeversolar_local.zeversolar_api import ZeverSolarApiClient

from unittest.mock import patch

from zeversolarlocal import ZeverError, ZeverTimeout

from homeassistant.helpers.update_coordinator import UpdateFailed

from pytest_homeassistant_custom_component.common import MockConfigEntry

import pytest

async def test_ZeverSolarApiClient_class(hass):
    """Simple test for construction and initialization"""
    host = "TEST_HOST"

    result_api = ZeverSolarApiClient(host)
    assert type(result_api) is ZeverSolarApiClient

async def test_ZeverSolarApiClient_async_get_id_ok(hass):
    """Simple test for construction and initialization"""
    host = "TEST_HOST"

    result_api = ZeverSolarApiClient(host)

    with patch("custom_components.zeversolar_local.zeversolar_api.zs.inverter_id") as api_mock:
        expected_id = "abcd"
        api_mock.return_value = expected_id

        result_id = await result_api.async_get_id()

        assert expected_id == result_id

async def test_ZeverSolarApiClient_async_get_id_ok(hass):
    """Simple test for construction and initialization"""
    host = "TEST_HOST"

    result_api = ZeverSolarApiClient(host)

    with patch("custom_components.zeversolar_local.zeversolar_api.zs.solardata") as api_mock:
        expected_data = "any_object"
        api_mock.return_value = expected_data

        result_data = await result_api.async_get_data()

        assert expected_data == result_data

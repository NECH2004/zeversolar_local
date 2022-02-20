"""Test component setup."""
from homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryNotReady

from custom_components.zeversolar_local.const import DOMAIN

from custom_components.zeversolar_local.__init__ import async_setup_entry, async_unload_entry, async_reload_entry, async_options_update_listener

from custom_components.zeversolar_local.zeversolar_api import ZeverSolarApiClient
from custom_components.zeversolar_local.coordinator import ZeversolarApiCoordinator

from unittest.mock import patch
from pytest_homeassistant_custom_component.common import MockConfigEntry, mock_integration, MockModule

import pytest

async def test_async_setup_entry_config_not_ready(hass):
    with pytest.raises(ConfigEntryNotReady):

        """Test the integration setup with no connection to the inverter throwning a ConfigEntryNotReady exception"""
        mock_integration(hass, MockModule(DOMAIN))

        config_entry = MockConfigEntry(
            domain=DOMAIN,
            unique_id="my_unique_test_id",
            data={
                CONF_HOST: "TEST_HOST"
            },
        )
    
        config_entry.add_to_hass(hass)

        await async_setup_entry(hass, config_entry)
    
async def test_async_setup_entry_domain_not_loaded(hass):
    """Test the integration setup with no domain data"""

    mock_integration(hass, MockModule(DOMAIN))

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        },
    )
        
    config_entry.add_to_hass(hass)

    # name is zeversolarlocal.api - see manifest, zeversolarlocal is aliased as zs.
    with patch("custom_components.zeversolar_local.zeversolar_api.zs.solardata") as api_mock:
        api_mock.return_value = "Test"
        test_result = await async_setup_entry(hass, config_entry)
        assert test_result is True

async def test_async_setup_entry_domain_already_loaded(hass):
    """Test the integration setup with domain data"""

    hass.data.setdefault(DOMAIN, {})
    mock_integration(hass, MockModule(DOMAIN))

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        },
    )
    
    config_entry.add_to_hass(hass)

    with patch("custom_components.zeversolar_local.zeversolar_api.zs.solardata") as api_mock:
        api_mock.return_value = "any_value"
        test_result = await async_setup_entry(hass, config_entry)
        assert test_result is True

async def test_async_setup_entry_domain_already_loaded_mock_coordinator(hass):
    """Test the integration setup with domain data"""

    hass.data.setdefault(DOMAIN, {})
    mock_integration(hass, MockModule(DOMAIN))

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        },
    )
    
    config_entry.add_to_hass(hass)

    with patch("custom_components.zeversolar_local.coordinator.ZeversolarApiCoordinator._async_update_data") as api_mock:
        api_mock.return_value = "any_value"
        test_result = await async_setup_entry(hass, config_entry)
        assert test_result is True

async def test_async_unload_entry_all_can_be_unloaded(hass):
    """Test to unload the integration"""

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        }
    )

    client = ZeverSolarApiClient("HOST")
    coordinator = ZeversolarApiCoordinator(hass, client=client)

    mock_integration(hass, MockModule(DOMAIN))
    config_entry.add_to_hass(hass)
    hass.data.setdefault(DOMAIN, {config_entry.entry_id: coordinator})

    test_result = await async_unload_entry(hass, config_entry)
    assert test_result is True

async def test_async_reload_entry(hass):
    """Test to relod the config entry"""

    mock_integration(hass, MockModule(DOMAIN))

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        },
    )
        
    config_entry.add_to_hass(hass)

    # name is zeversolarlocal.api - see manifest, zeversolarlocal is aliased as zs.
    with patch("custom_components.zeversolar_local.zeversolar_api.zs.solardata") as api_mock:
        api_mock.return_value = "foo_value"
        # must setup the entry first
        await async_setup_entry(hass, config_entry)

        # act
        await async_reload_entry(hass, config_entry)

    result_entry = hass.data[DOMAIN].pop(config_entry.entry_id)

    # assert
    assert type(result_entry) is ZeversolarApiCoordinator

async def test_async_options_update_listener(hass):
    """Test the options update listener"""

    mock_integration(hass, MockModule(DOMAIN))

    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="my_unique_test_id",
        data={
            CONF_HOST: "TEST_HOST"
        },
    )

    config_entry.add_to_hass(hass)

    with patch("homeassistant.config_entries.ConfigEntries.async_reload") as method_mock:
        # act
        await async_options_update_listener(hass, config_entry)

        # assert
        method_mock.assert_called_once()


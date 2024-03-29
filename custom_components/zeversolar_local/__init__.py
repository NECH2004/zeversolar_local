"""integrates a Zeversolar inverter to Home Assistant using its local API."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    CONF_SERIAL_NO,
    DOMAIN,
    ENTRY_COORDINATOR,
    ENTRY_DEVICE_INFO,
    OPT_DATA_INTERVAL,
    OPT_DATA_INTERVAL_VALUE,
    PLATFORMS,
    STARTUP_MESSAGE,
)
from .coordinator import ZeversolarApiCoordinator
from .zever_local import ZeverSolarApiClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    # Set up Zeversolar Inverter local from a config entry.
    host = entry.data.get(CONF_HOST)
    # zever_id = entry.data.get(CONF_SERIAL_NO)

    data_interval = entry.options.get(OPT_DATA_INTERVAL, OPT_DATA_INTERVAL_VALUE)

    client = ZeverSolarApiClient(host)

    try:
        await client.inverter.async_connect()
        coordinator = ZeversolarApiCoordinator(hass, client=client)
        coordinator.update_interval = timedelta(seconds=data_interval)
        await coordinator.async_refresh()

        if not coordinator.last_update_success:
            raise ConfigEntryNotReady

    except Exception as err:
        raise ConfigEntryNotReady from err

    serial_number = entry.data[CONF_SERIAL_NO]

    inverter_data = await coordinator.client.async_get_data()
    hardware_version = inverter_data.hardware_version
    software_version = inverter_data.software_version

    device_info = DeviceInfo(
        configuration_url=f"http://{host}",
        # default_manufacturer: str
        # default_model: str
        # default_name: str
        # entry_type: DeviceEntryType | None
        identifiers={(DOMAIN, serial_number)},
        manufacturer="Zeversolar",
        # model: str | None
        name=f"Zeversolar inverter '{serial_number}'",
        # suggested_area: str | None
        sw_version=software_version,
        hw_version=hardware_version,
        # via_device: tuple[str, str]
    )

    # Store the deviceinfo and coordinator object for the platforms to access
    hass.data[DOMAIN][entry.entry_id] = {
        ENTRY_COORDINATOR: coordinator,
        ENTRY_DEVICE_INFO: device_info,
    }

    for platform in PLATFORMS:
        coordinator.platforms.append(platform)
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    # Wait to install the reload listener until everything was successfully initialized
    entry.async_on_unload(entry.add_update_listener(async_options_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id][ENTRY_COORDINATOR]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_options_update_listener(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

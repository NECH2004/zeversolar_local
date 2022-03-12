"""The Zeversolar Inverter local coordinator."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, OPT_DATA_INTERVAL_VALUE
from .zever_local import ZeverSolarApiClient

_LOGGER = logging.getLogger(__name__)


class ZeversolarApiCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: ZeverSolarApiClient) -> None:
        """Initialize."""
        self.client = client
        self.platforms = []

        super().__init__(
            # update_inverval is set in async_setup_entry()
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=OPT_DATA_INTERVAL_VALUE),
        )

    async def _async_update_data(self):
        """Update data via API."""
        try:
            self.last_update_success = True
            return await self.client.async_get_data()
        except Exception as exception:
            self.logger.debug("Zeversolar get_data() error. %s", exception)
            self.last_update_success = False

            raise UpdateFailed() from exception

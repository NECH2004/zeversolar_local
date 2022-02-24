"""Wraps the API to connect to a ZeverSolar inverter locally."""
import logging

import zeversolarlocal as zs

_LOGGER: logging.Logger = logging.getLogger(__package__)


# ZeverSolar local API Client."""
class ZeverSolarApiClient:
    """Wraps the ZeverSolar API"""

    # Initialize the class
    def __init__(self, host: str) -> None:
        self._url = zs.default_url(host)

    async def async_get_id(self):
        """Gets the inverter id"""
        return await zs.inverter_id(self._url)

    async def async_get_data(self):
        """Gets the data"""
        return await zs.solardata(self._url)

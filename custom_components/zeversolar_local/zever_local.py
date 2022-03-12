"""Wraps the API to connect to a Zeversolar inverter locally."""
import logging

from zever_local.inverter import Inverter, InverterData

_LOGGER: logging.Logger = logging.getLogger(__package__)


# Zeversolar local API Client."""
class ZeverSolarApiClient:
    """Wraps the Zeversolar local API"""

    _inverter: Inverter = None

    # Initialize the class
    def __init__(self, host: str, timeout: int = 5) -> None:
        self._inverter = Inverter(host, timeout=timeout)

    async def async_get_id(self):
        """Gets the inverter id"""
        await self._inverter.async_connect()
        return self._inverter.mac_address

    async def async_get_data(self) -> InverterData:
        """Gets the data"""
        inverter_data = await self._inverter.async_get_data()
        return inverter_data

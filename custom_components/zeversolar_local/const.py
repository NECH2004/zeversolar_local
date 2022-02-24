"""Constants for the ZeverSolar Inverter local integration."""
from homeassistant.const import Platform

# Base component constants
NAME = "ZeverSolar Local Integration"
DEVICE_NAME = "ZeverSolar Inverter"
DEVICE_MODEL = "Universal Inverter Device"
MANUFACTURER_NAME = "ZeverSolar"

ISSUE_URL = "https://github.com/nech/zeversolar_local/issues"

"""The domain name."""
DOMAIN = "zeversolar_local"
DOMAIN_DATA = f"{DOMAIN}_data"

CONF_SERIAL_NO = "zever_serial_number"

OPT_DATA_INTERVAL = "zever_data_interval"
OPT_DATA_INTERVAL_VALUE: int = 30

SENSOR_DAILY_ENERGY = "daily_energy"
SENSOR_CURRENT_POWER = "current_power"


"""The actual version of the integration."""
VERSION = "0.0.1"

"""List of platforms that are supported."""
PLATFORMS = [Platform.SENSOR]

# Additional
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
Fetch data from a ZeverSolar inverter using its local API.
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
DOMAIN = "zeversolar_local"

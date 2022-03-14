"""Constants for the Zeversolar Inverter local integration."""
from homeassistant.const import Platform

# Base component constants
NAME = "Zeversolar Local Integration"
DEVICE_NAME = "Zeversolar Inverter"
DEVICE_MODEL = "Universal Inverter Device"
MANUFACTURER_NAME = "Zeversolar"

ISSUE_URL = "https://github.com/nech/zeversolar_local/issues"

"""The domain name."""
DOMAIN = "zeversolar_local"
DOMAIN_DATA = f"{DOMAIN}_data"

CONF_SERIAL_NO = "zever_serial_number"

ENTRY_COORDINATOR = "zever_coordinator"
ENTRY_DEVICE_INFO = "zever_device_info"

OPT_DATA_INTERVAL = "zever_data_interval"
OPT_DATA_INTERVAL_VALUE: int = 30


"""The actual version of the integration."""
VERSION = "1.1.0"

"""List of platforms that are supported."""
PLATFORMS = [Platform.SENSOR, Platform.BUTTON]

# Additional
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
Fetch data from a Zeversolar inverter using its local API.
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
DOMAIN = "zeversolar_local"

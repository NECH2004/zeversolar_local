"""Config flow for Zeversolar Inverter local API."""
import logging

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import callback
import voluptuous as vol
from zever_local.inverter import ZeversolarError, ZeversolarTimeout

from .const import CONF_SERIAL_NO, DOMAIN, OPT_DATA_INTERVAL, OPT_DATA_INTERVAL_VALUE
from .zever_local import ZeverSolarApiClient

_LOGGER = logging.getLogger(__name__)


class ZeverSolarFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Zeversolar local API integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:

            try:
                zever_id = await self._get_id(user_input[CONF_HOST])
            except ZeversolarTimeout as exception:
                _LOGGER.debug("fetching Zeversolar inverter id failed - %s", exception)
                return self.async_abort(reason="invalid_inverter")

            except ZeversolarError as exception:
                _LOGGER.debug("fetching Zeversolar inverter id failed - %s", exception)
                self._errors["base"] = "error_inverter"
                return await self._show_config_form()

            except Exception as exception:  # pylint: disable=broad-except
                _LOGGER.debug(
                    "fetching Zeversolar inverter id failed witch general exception - %s",
                    exception,
                )
                return self.async_abort(reason="invalid_inverter")

            for config_entry in self._async_current_entries():
                my_data = config_entry.data
                my_id = my_data.get(CONF_SERIAL_NO)

                if my_id == zever_id:
                    return self.async_abort(reason="duplicate_inverter")

            return self.async_create_entry(
                title=f"Zeversolar Inverter '{zever_id}'",
                data={CONF_HOST: user_input[CONF_HOST], CONF_SERIAL_NO: zever_id},
            )

        return await self._show_config_form()

    async def _show_config_form(self):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=self._errors,
        )

    async def _get_id(self, host) -> str:
        """Return true if credentials is valid."""
        client = ZeverSolarApiClient(host)
        zever_id = await client.async_get_id()
        return zever_id

    async def _test_url(self, host):
        """Return true if credentials is valid."""
        try:
            client = ZeverSolarApiClient(host)
            zever_id = await client.async_get_id()
            return zever_id is not None
        except Exception:  # pylint: disable=broad-except
            pass
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ZeverSolarOptionsFlowHandler(config_entry)


class ZeverSolarOptionsFlowHandler(config_entries.OptionsFlow):
    """Defines the configurable options for a Zeversolar inverter"""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        _errors: dict[str, str] = {}

        if user_input is not None:
            new_data_interval = user_input[OPT_DATA_INTERVAL]
            _LOGGER.debug("New data interval was set to %s", new_data_interval)

            if new_data_interval is None:
                _LOGGER.debug("New data interval is none")
                _errors["base"] = "data_interval_empty"

            elif not 10 <= new_data_interval <= 3600:
                _LOGGER.debug("New data interval is wrong (out of limits)")
                _errors["base"] = "data_interval_wrong"

            else:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        OPT_DATA_INTERVAL,
                        default=self.config_entry.options.get(
                            OPT_DATA_INTERVAL, OPT_DATA_INTERVAL_VALUE
                        ),
                    ): int,
                }
            ),
            errors=_errors,
        )

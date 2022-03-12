"""Sensor platform for Zeversolar inverter."""
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from zever_local.inverter import Inverter

from .const import DOMAIN, ENTRY_COORDINATOR
from .coordinator import ZeversolarApiCoordinator

# not needed
# SCAN_INTERVAL = timedelta(seconds=30)

PARALLEL_UPDATES = 1


@dataclass
class ZeversolarButtonEntityDescriptionMixin:
    """Mixin to describe a Zeversolar button entity."""

    press_action: Awaitable[Callable[[Inverter], None]]


@dataclass
class ZeversolarButtonEntityDescription(
    ButtonEntityDescription, ZeversolarButtonEntityDescriptionMixin
):
    """Class to describe a Zeversolar button entity."""


BUTTON_POWER_ON_ENTITY_DESCRIPTION = ZeversolarButtonEntityDescription(
    key="power_on",
    press_action=lambda device: device.power_on(),
    icon="mdi:dip-switch",
)
BUTTON_POWER_OFF_ENTITY_DESCRIPTION = ZeversolarButtonEntityDescription(
    key="power_off",
    press_action=lambda device: device.power_off(),
    icon="mdi:lightbulb",
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Setup button platform."""
    zever_coordinator: ZeversolarApiCoordinator = hass.data[DOMAIN][entry.entry_id][
        ENTRY_COORDINATOR
    ]
    inverter = zever_coordinator.client.inverter

    power_on_button = ZeverSolarButton(inverter, BUTTON_POWER_ON_ENTITY_DESCRIPTION)
    power_off_button = ZeverSolarButton(inverter, BUTTON_POWER_OFF_ENTITY_DESCRIPTION)

    entities = [power_on_button, power_off_button]
    async_add_entities(entities)


class ZeverSolarButton(ButtonEntity):
    """Entity representing individual inverter sensor."""

    _entity_description: ZeversolarButtonEntityDescription

    def __init__(
        self, inverter: Inverter, entity_description: ZeversolarButtonEntityDescription
    ) -> None:
        """Initialize an inverter button."""
        self._entity_description = entity_description
        self._inverter = inverter

    async def async_press(self) -> None:
        """Perform the button action."""
        await self._entity_description.press_action(self._inverter)

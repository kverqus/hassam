import logging

from typing import Union
from datetime import datetime

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.const import (
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME
)

from .ssam_api import SSAMAPI
from .const import (
    DOMAIN,
    DEVICE_NAME,
    DEVICE_AUTHOR,
    DEVICE_VERSION,
    SENSOR_ATTRIB,
    SCAN_INTERVAL
)

_LOGGER = logging.getLogger(f'custom_components.{DOMAIN}.core')


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities
) -> None:
    ssam_api = SSAMAPI()
    schedule_list = await ssam_api.get_schedule(config_entry.data.get('building_address'))

    for schedule in schedule_list:
        async_add_entities(
            [ScheduleSensor(hass=hass, config=config_entry, schedule=schedule)],
            update_before_add=True
        )


class ScheduleSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, config: ConfigEntry, schedule: dict):
        self.hass = hass
        self._config = config
        self._title = config.title
        self._state = None
        self._available = True
        self._schedule = schedule

        self._attr_unique_id = f'{DOMAIN}_{self._schedule['bin_code']}_{self._config.data.get("id")}'
        self._attr_name = f'SSAM {self._title} {self._schedule['waste_type']}'
        self._attr_icon = 'mdi:trash-can-outline'
        self._attr_attribution = SENSOR_ATTRIB
        self._attr_device_info = {
            ATTR_IDENTIFIERS: {(DOMAIN, DEVICE_NAME)},
            ATTR_NAME: DEVICE_NAME,
            ATTR_MANUFACTURER: DEVICE_AUTHOR,
            ATTR_MODEL: f'v{DEVICE_VERSION}',
            'entry_type': DeviceEntryType.SERVICE
        }

    async def async_update(self) -> None:
        bin_code = self._attr_unique_id.split('_')[1]
        ssam_api = SSAMAPI()
        schedule_list = await ssam_api.get_schedule(self._config.options.get('building_address', self._config.data['building_address']))

        for schedule in schedule_list:
            if schedule['bin_code'] == bin_code:
                self._schedule = schedule

        if not self._schedule:
            self._available = False
            return False

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attributes = {
            'last_update': timestamp,
            'friendly_name': self._title,
            **self._schedule
        }

        self._attr_extra_state_attributes = attributes
        self._state = timestamp

        _LOGGER.debug(f'[hassam updater] Entity {self._attr_name} has been updated')

    @property
    def available(self) -> bool:
        return self._available

    @property
    def state(self) -> Union[None, str]:
        return self._state

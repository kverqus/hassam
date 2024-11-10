import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType

from .ssam_api import SSAMAPI
from .const import DOMAIN, PLATFORMS, SCAN_INTERVAL

_LOGGER = logging.getLogger(f'custom_components.{DOMAIN}.core')


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    _LOGGER.debug('[setup] Entering')

    @callback
    async def find_address(service):
        _LOGGER.debug('[find_address] Entered')
        search_string = service.data.get('search_string')
        _LOGGER.debug(f'[find_address] Looking for "{search_string}"')

        try:
            ssam_api = SSAMAPI()
            result = await ssam_api.search_address(search_string)
            _LOGGER.debug('[find_address] Completed')
            hass.bus.fire(DOMAIN, {
                'source': 'find_address',
                'state': 'success',
                'result': result
            })
            return True

        except Exception as err:
            _LOGGER.debug('[find_address] Lookup failed')
            hass.bus.fire(DOMAIN, {
                'source': 'find_address',
                'state': 'error',
                'result': f'An exception occured during lookup: {str(err)}'
            })
            return True

    @callback
    async def event_listener(service):
        _LOGGER.debug('[eventListener] Entered')

        command = service.data.get('cmd')

        if command == 'find_address':
            find_address(service)
            _LOGGER('[eventListener] Dispatched to find_address')
            return True

    if DOMAIN not in hass.data:
        hass.data.setdefault(DOMAIN, {})

    _LOGGER.debug('[setup] Registering services')
    try:
        hass.services.async_register(DOMAIN, 'find_address', find_address)
        _LOGGER.debug('[setup] Service registration completed')
    except:
        _LOGGER.error('[setup] Service registration failed')

    _LOGGER.debug('[setup] Registering event listeners')
    try:
        hass.bus.async_listen(DOMAIN, event_listener)
        _LOGGER.debug('[setup] Registering event listener completed')
    except:
        _LOGGER.error('[setup] Registering event listener failed')

    _LOGGER.debug('[setup] Completed')
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # When the configuration options are being updated we want to automatically
    # reload the integration so that the new options take effect immediately
    _LOGGER.debug('[config] Reloading integration')
    entry.async_on_unload(entry.add_update_listener(update_listener))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    _LOGGER.error('[update] Update listener running')
    hass.async_create_task(hass.config_entries.async_reload(entry.entry_id))
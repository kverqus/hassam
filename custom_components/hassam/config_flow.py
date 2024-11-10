import logging
import uuid

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from typing import Any
from .const import DOMAIN, CONF_NAME

_LOGGER = logging.getLogger(f'custom_components.{DOMAIN}.core')

CONF_SCHEMA = vol.Schema({('config_name'): str})
DATA_SCHEMA = vol.Schema({('building_address'): str})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    return data

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        _LOGGER.debug("[async_step_user] Entered")
        errors = {}

        if user_input is None:
            _LOGGER.debug("[async_step_user] Showing creation form")
            return self.async_show_form(
                step_id='user',
                data_schema=CONF_SCHEMA
            )

        try:
            user_input = await validate_input(self.hass, user_input)
        except Exception as err:
            errors['base'] = f'unknown, {str(err)}'
            _LOGGER.debug(
                f'[setup_integration(validate)] Unknown exception occured: {str(err)}'
            )
            return self.async_show_form(
                step_id='user',
                data_schema=CONF_SCHEMA,
                errors=errors
            )

        self._userdata = user_input

        return self.async_show_form(
            step_id='config',
            data_schema=DATA_SCHEMA,
            errors=errors
        )

    async def async_step_config(self, user_input: dict[str, Any] | None = None):
        _LOGGER.debug("[async_step_config] Entered")
        errors = {}

        if user_input is not None:
            try:
                user_input = await validate_input(self.hass, user_input)
            except Exception as err:
                errors['base'] = f'unknown, {str(err)}'
                _LOGGER.debug(
                    f'[setup_integration_config(validate)] Unknown exception occured: {str(err)}'
                )
            else:
                try:
                    unique_id = str(uuid.uuid4())
                    await self.async_set_unique_id(unique_id)
                    self._abort_if_unique_id_configured()
                    user_input['id'] = unique_id

                    return self.async_create_entry(
                        title=self._userdata['config_name'],
                        data=user_input
                    )
                except Exception as err:
                    _LOGGER.error(f'[setup_integration] Entry creation failed for {self._name}: {str(err)}')
                    return self.async_abort(reason='not_supported')

            return self.async_show_form(
                step_id='config',
                data_schema=DATA_SCHEMA,
                errors=errors
            )

        return self.async_show_form(
            step_id='config',
            data_schema=DATA_SCHEMA
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def validate_input(self, data: str) -> str:
        return data

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        UPDATE_SCHEMA = vol.Schema({
            vol.Optional('building_address', default=self.config_entry.options.get('building_address', self.config_entry.data['building_address'])): str
        })

        if user_input is None:
            return self.async_show_form(step_id='user', data_schema=UPDATE_SCHEMA)

        return self.async_create_entry(
            title=self.config_entry.title,
            data=user_input
        )
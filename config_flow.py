"""Config flow for Buienradar Regenradar integration."""
from __future__ import annotations

import voluptuous as vol
from typing import Any, Dict, Optional

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN, DEFAULT_NAME, CONF_IMAGE_REFRESH_SECONDS

class BuienradarRadarConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Buienradar Regenradar."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate user input
            # Since this is a simple integration with no actual validation needed,
            # we can just create the entry

            # Check if we already have an entry with this name
            await self.async_set_unique_id(f"buienradar_radar_{user_input[CONF_NAME]}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        # If there is no user input or there were errors, show the form again
        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_IMAGE_REFRESH_SECONDS, default=300): vol.All(
                    int, vol.Range(min=60, max=3600)
                ),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return BuienradarRadarOptionsFlow(config_entry)

class BuienradarRadarOptionsFlow(OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IMAGE_REFRESH_SECONDS,
                        default=self.config_entry.options.get(
                            CONF_IMAGE_REFRESH_SECONDS,
                            self.config_entry.data.get(CONF_IMAGE_REFRESH_SECONDS, 300),
                        ),
                    ): vol.All(int, vol.Range(min=60, max=3600)),
                }
            ),
        )
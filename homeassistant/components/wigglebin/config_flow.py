"""Config flow for WiggleBin integration."""

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback

from .const import DOMAIN


class WiggleBinConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WiggleBin."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict = {}
        if user_input is not None:
            # Validate user input here if necessary
            return self.async_create_entry(title="WiggleBin", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return WiggleBinOptionsFlowHandler(config_entry)


class WiggleBinOptionsFlowHandler(OptionsFlow):
    """Handle WiggleBin options."""

    def __init__(self, config_entry) -> None:
        """Initialize WiggleBin options."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> ConfigFlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )

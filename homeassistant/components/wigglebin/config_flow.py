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

DEFAULT_NAME = "WiggleBin"
DEFAULT_API_URL = "http://wigglebin.local:5000"


class WiggleBinConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WiggleBin."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict = {}
        if user_input is not None:
            # Validate user input here if necessary
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name", default=DEFAULT_NAME): str,
                    vol.Required("api_url", default=DEFAULT_API_URL): str,
                }
            ),
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
        errors: dict = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_data = self.config_entry.data

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "name", default=current_data.get("name", DEFAULT_NAME)
                    ): str,
                    vol.Required(
                        "api_url", default=current_data.get("api_url", DEFAULT_API_URL)
                    ): str,
                }
            ),
            errors=errors,
        )

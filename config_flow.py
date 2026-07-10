"""Config flow for Tasmota Timer Configuration integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, DEFAULT_NAME, CONF_DEVICE_TOPICS

_LOGGER = logging.getLogger(__name__)


class TasmotaTimersConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tasmota Timer Configuration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title=DEFAULT_NAME, data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
            description_placeholders={
                "info": "This integration provides services to configure Tasmota device timers via MQTT."
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return TasmotaTimersOptionsFlow()


class TasmotaTimersOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Tasmota Timer Configuration."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            topics = [
                topic.strip()
                for topic in user_input.get(CONF_DEVICE_TOPICS, "").split(",")
                if topic.strip()
            ]
            return self.async_create_entry(
                title="",
                data={CONF_DEVICE_TOPICS: ",".join(topics)},
            )

        current_topics = self.config_entry.options.get(CONF_DEVICE_TOPICS, "")

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_DEVICE_TOPICS,
                    default=current_topics,
                ): str,
            }),
            description_placeholders={
                "info": "Comma-separated list of Tasmota device topics to create entities for, in addition to auto-discovered devices."
            }
        )

"""The Tasmota Timer Configuration integration."""
import logging
import json

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.components import mqtt

from .const import (
    DOMAIN,
    CONF_DEVICE_TOPIC,
    CONF_DEVICE_TOPICS,
    CONF_TIMER_INDEX,
    SERVICE_SET_TIMER,
    SERVICE_ENABLE_TIMER,
    SERVICE_DISABLE_TIMER,
    SERVICE_ENABLE_ALL_TIMERS,
    SERVICE_DISABLE_ALL_TIMERS,
    SERVICE_GET_TIMERS,
    ATTR_TIMER_ENABLE,
    ATTR_TIMER_TIME,
    ATTR_TIMER_WINDOW,
    ATTR_TIMER_DAYS,
    ATTR_TIMER_REPEAT,
    ATTR_TIMER_OUTPUT,
    ATTR_TIMER_ACTION,
    ATTR_DEVICE_MAC,
    ATTR_DEVICE_TOPIC,
    ATTR_DEVICE_NAME,
    CONF_DEVICES,
    DISCOVERY_TASMOTA_CONFIG_TOPIC,
    DISCOVERY_LWT_TOPIC,
    DISCOVERY_STATE_TOPIC,
)

_LOGGER = logging.getLogger(__name__)

SET_TIMER_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
    vol.Required(CONF_TIMER_INDEX): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
    vol.Optional(ATTR_TIMER_ENABLE, default=1): vol.All(vol.Coerce(int), vol.In([0, 1])),
    vol.Optional(ATTR_TIMER_TIME): cv.string,
    vol.Optional(ATTR_TIMER_WINDOW, default=0): vol.All(vol.Coerce(int), vol.Range(min=0, max=15)),
    vol.Optional(ATTR_TIMER_DAYS): cv.string,
    vol.Optional(ATTR_TIMER_REPEAT, default=1): vol.All(vol.Coerce(int), vol.In([0, 1])),
    vol.Optional(ATTR_TIMER_OUTPUT, default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=8)),
    vol.Optional(ATTR_TIMER_ACTION, default=1): vol.All(vol.Coerce(int), vol.In([0, 1, 2, 3])),
})

ENABLE_TIMER_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
    vol.Required(CONF_TIMER_INDEX): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
})

DISABLE_TIMER_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
    vol.Required(CONF_TIMER_INDEX): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
})

GET_TIMERS_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
    vol.Optional(CONF_TIMER_INDEX): vol.All(vol.Coerce(int), vol.Range(min=1, max=16)),
})

ENABLE_ALL_TIMERS_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
})

DISABLE_ALL_TIMERS_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_TOPIC): cv.string,
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tasmota Timer Configuration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    entry_data = hass.data[DOMAIN][entry.entry_id] = {
        "devices": {},
        "add_entities_callback": None,
    }

    # Restore devices persisted from previous runs
    persisted_devices = entry.data.get(CONF_DEVICES, {})
    if isinstance(persisted_devices, dict):
        for device_topic, device_info in persisted_devices.items():
            if isinstance(device_info, dict):
                entry_data["devices"][device_topic] = {
                    ATTR_DEVICE_NAME: device_info.get(ATTR_DEVICE_NAME, device_topic),
                    ATTR_DEVICE_MAC: device_info.get(ATTR_DEVICE_MAC),
                }

    async def _save_devices() -> None:
        """Persist currently known devices to the config entry."""
        devices_to_save = {
            topic: {
                ATTR_DEVICE_TOPIC: topic,
                ATTR_DEVICE_NAME: info.get(ATTR_DEVICE_NAME, topic),
                ATTR_DEVICE_MAC: info.get(ATTR_DEVICE_MAC),
            }
            for topic, info in entry_data["devices"].items()
        }
        new_data = {**entry.data, CONF_DEVICES: devices_to_save}
        hass.config_entries.async_update_entry(entry, data=new_data)

    async def _discover_device(
        device_topic: str, device_name: str | None = None, device_mac: str | None = None
    ) -> None:
        """Add a newly discovered Tasmota device and create its switch entity."""
        if not device_topic or device_topic in entry_data["devices"]:
            return

        entry_data["devices"][device_topic] = {
            ATTR_DEVICE_NAME: device_name or device_topic,
            ATTR_DEVICE_MAC: device_mac,
        }
        await _save_devices()
        add_callback = entry_data["add_entities_callback"]
        if add_callback:
            from .switch import TasmotaTimersSwitch
            add_callback(
                [
                    TasmotaTimersSwitch(
                        hass,
                        device_topic,
                        device_name=device_name or device_topic,
                        device_mac=device_mac,
                    )
                ]
            )
            _LOGGER.info(
                f"Discovered Tasmota device: {device_topic}"
                f"{f' ({device_name})' if device_name else ''}"
            )

    async def _tasmota_discovery_callback(msg) -> None:
        """Handle Tasmota discovery config messages."""
        try:
            payload = json.loads(msg.payload)
        except (ValueError, TypeError):
            return

        if not isinstance(payload, dict):
            return

        device_topic = payload.get("t")
        if not device_topic:
            return

        device_mac = payload.get("mac")
        device_name = payload.get("dn") or device_topic

        await _discover_device(device_topic, device_name=device_name, device_mac=device_mac)

    async def _fallback_discovery_callback(msg) -> None:
        """Handle fallback MQTT discovery via LWT and STATE topics."""
        topic_parts = msg.topic.split("/")
        if len(topic_parts) < 3:
            return
        device_topic = topic_parts[1]
        await _discover_device(device_topic)

    await mqtt.async_subscribe(
        hass, DISCOVERY_TASMOTA_CONFIG_TOPIC, _tasmota_discovery_callback
    )
    await mqtt.async_subscribe(hass, DISCOVERY_LWT_TOPIC, _fallback_discovery_callback)
    await mqtt.async_subscribe(hass, DISCOVERY_STATE_TOPIC, _fallback_discovery_callback)

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SWITCH])

    manual_topics = entry.options.get(CONF_DEVICE_TOPICS, "")
    for device_topic in (
        topic.strip() for topic in manual_topics.split(",") if topic.strip()
    ):
        await _discover_device(device_topic)

    async def handle_set_timer(call: ServiceCall) -> None:
        """Handle the set_timer service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        timer_index = call.data[CONF_TIMER_INDEX]
        
        timer_data = {
            "Enable": call.data.get(ATTR_TIMER_ENABLE, 1),
            "Mode": 0,
            "Time": call.data.get(ATTR_TIMER_TIME, "00:00"),
            "Window": call.data.get(ATTR_TIMER_WINDOW, 0),
            "Days": call.data.get(ATTR_TIMER_DAYS, "1111111"),
            "Repeat": call.data.get(ATTR_TIMER_REPEAT, 1),
            "Output": call.data.get(ATTR_TIMER_OUTPUT, 1),
            "Action": call.data.get(ATTR_TIMER_ACTION, 1),
        }
        
        command = f"Timer{timer_index}"
        payload = json.dumps(timer_data)
        
        topic = f"cmnd/{device_topic}/{command}"
        
        _LOGGER.info(f"Setting timer {timer_index} on {device_topic}: {payload}")
        
        await mqtt.async_publish(hass, topic, payload)

    async def handle_enable_timer(call: ServiceCall) -> None:
        """Handle the enable_timer service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        timer_index = call.data[CONF_TIMER_INDEX]
        
        command = f"Timer{timer_index}"
        topic = f"cmnd/{device_topic}/{command}"
        payload = json.dumps({"Enable": 1})
        
        _LOGGER.info(f"Enabling timer {timer_index} on {device_topic}")
        
        await mqtt.async_publish(hass, topic, payload)

    async def handle_disable_timer(call: ServiceCall) -> None:
        """Handle the disable_timer service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        timer_index = call.data[CONF_TIMER_INDEX]
        
        command = f"Timer{timer_index}"
        topic = f"cmnd/{device_topic}/{command}"
        payload = json.dumps({"Enable": 0})
        
        _LOGGER.info(f"Disabling timer {timer_index} on {device_topic}")
        
        await mqtt.async_publish(hass, topic, payload)

    async def handle_enable_all_timers(call: ServiceCall) -> None:
        """Handle the enable_all_timers service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        topic = f"cmnd/{device_topic}/Timers"
        
        _LOGGER.info(f"Enabling all timers on {device_topic}")
        
        await mqtt.async_publish(hass, topic, "1")

    async def handle_disable_all_timers(call: ServiceCall) -> None:
        """Handle the disable_all_timers service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        topic = f"cmnd/{device_topic}/Timers"
        
        _LOGGER.info(f"Disabling all timers on {device_topic}")
        
        await mqtt.async_publish(hass, topic, "0")

    async def handle_get_timers(call: ServiceCall) -> None:
        """Handle the get_timers service call."""
        device_topic = call.data[CONF_DEVICE_TOPIC]
        timer_index = call.data.get(CONF_TIMER_INDEX)
        
        if timer_index:
            command = f"Timer{timer_index}"
        else:
            command = "Timers"
        
        topic = f"cmnd/{device_topic}/{command}"
        
        _LOGGER.info(f"Requesting timers from {device_topic}")
        
        await mqtt.async_publish(hass, topic, "")

    hass.services.async_register(
        DOMAIN, SERVICE_SET_TIMER, handle_set_timer, schema=SET_TIMER_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_ENABLE_TIMER, handle_enable_timer, schema=ENABLE_TIMER_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_DISABLE_TIMER, handle_disable_timer, schema=DISABLE_TIMER_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_ENABLE_ALL_TIMERS, handle_enable_all_timers, schema=ENABLE_ALL_TIMERS_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_DISABLE_ALL_TIMERS, handle_disable_all_timers, schema=DISABLE_ALL_TIMERS_SCHEMA
    )
    
    hass.services.async_register(
        DOMAIN, SERVICE_GET_TIMERS, handle_get_timers, schema=GET_TIMERS_SCHEMA
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, [Platform.SWITCH])

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    hass.services.async_remove(DOMAIN, SERVICE_SET_TIMER)
    hass.services.async_remove(DOMAIN, SERVICE_ENABLE_TIMER)
    hass.services.async_remove(DOMAIN, SERVICE_DISABLE_TIMER)
    hass.services.async_remove(DOMAIN, SERVICE_ENABLE_ALL_TIMERS)
    hass.services.async_remove(DOMAIN, SERVICE_DISABLE_ALL_TIMERS)
    hass.services.async_remove(DOMAIN, SERVICE_GET_TIMERS)

    return unload_ok

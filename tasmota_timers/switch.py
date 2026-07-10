"""Switch platform for Tasmota Timer Configuration."""
import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Tasmota Timer switches."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    entry_data["add_entities_callback"] = async_add_entities

    entities = []
    for device_topic, device_info in entry_data["devices"].items():
        entities.append(
            TasmotaTimersSwitch(
                hass,
                device_topic,
                device_name=device_info.get("name", device_topic),
                device_mac=device_info.get("mac"),
            )
        )

    if entities:
        async_add_entities(entities)


class TasmotaTimersSwitch(SwitchEntity):
    """Switch representing the global timer enable state for a Tasmota device."""

    _attr_icon = "mdi:timer"
    _attr_should_poll = False

    def __init__(self, hass, device_topic, device_name=None, device_mac=None):
        """Initialise the switch."""
        self.hass = hass
        self._device_topic = device_topic
        self._device_name = device_name or device_topic
        self._device_mac = device_mac
        self._attr_has_entity_name = True
        self._attr_name = "Timers"
        if device_mac:
            self._attr_unique_id = f"{DOMAIN}_{device_mac}_timers_enabled"
        else:
            self._attr_unique_id = f"{DOMAIN}_{device_topic}_timers_enabled"
        self._attr_is_on = None
        self._attr_available = False
        self._unsub_lwt = None
        self._unsub_result = None

    @property
    def device_info(self):
        """Return device information."""
        identifiers = {(DOMAIN, self._device_mac or self._device_topic)}
        return DeviceInfo(
            identifiers=identifiers,
            name=self._device_name,
            manufacturer="Tasmota",
        )

    async def async_added_to_hass(self):
        """Subscribe to MQTT topics when added to Home Assistant."""
        self._unsub_lwt = await mqtt.async_subscribe(
            self.hass,
            f"tele/{self._device_topic}/LWT",
            self._handle_lwt,
        )
        self._unsub_result = await mqtt.async_subscribe(
            self.hass,
            f"stat/{self._device_topic}/RESULT",
            self._handle_result,
        )
        await mqtt.async_publish(
            self.hass, f"cmnd/{self._device_topic}/Timers", ""
        )

    async def async_will_remove_from_hass(self):
        """Unsubscribe from MQTT topics when removed."""
        if self._unsub_lwt:
            self._unsub_lwt()
            self._unsub_lwt = None
        if self._unsub_result:
            self._unsub_result()
            self._unsub_result = None

    async def _handle_lwt(self, msg):
        """Handle LWT messages for availability."""
        payload = msg.payload
        if payload == "Online":
            self._attr_available = True
            await mqtt.async_publish(
                self.hass, f"cmnd/{self._device_topic}/Timers", ""
            )
        elif payload == "Offline":
            self._attr_available = False
        self.async_write_ha_state()

    async def _handle_result(self, msg):
        """Handle RESULT messages for timer state."""
        try:
            payload = json.loads(msg.payload)
        except (ValueError, TypeError):
            return

        if not isinstance(payload, dict):
            return

        timers_value = payload.get("Timers")
        if timers_value is None:
            return

        timers_state = str(timers_value).upper()
        self._attr_is_on = timers_state in ("ON", "1", "TRUE", "YES")
        self._attr_available = True
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Enable all timers on the device."""
        await mqtt.async_publish(
            self.hass, f"cmnd/{self._device_topic}/Timers", "1"
        )
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Disable all timers on the device."""
        await mqtt.async_publish(
            self.hass, f"cmnd/{self._device_topic}/Timers", "0"
        )
        self._attr_is_on = False
        self.async_write_ha_state()

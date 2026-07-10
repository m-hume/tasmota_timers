"""Constants for the Tasmota Timer Configuration integration."""

DOMAIN = "tasmota_timers"
DEFAULT_NAME = "Tasmota Timers"

CONF_DEVICE_TOPIC = "device_topic"
CONF_TIMER_INDEX = "timer_index"

SERVICE_SET_TIMER = "set_timer"
SERVICE_ENABLE_TIMER = "enable_timer"
SERVICE_DISABLE_TIMER = "disable_timer"
SERVICE_ENABLE_ALL_TIMERS = "enable_all_timers"
SERVICE_DISABLE_ALL_TIMERS = "disable_all_timers"
SERVICE_GET_TIMERS = "get_timers"

ATTR_TIMER_ENABLE = "enable"
ATTR_TIMER_TIME = "time"
ATTR_TIMER_WINDOW = "window"
ATTR_TIMER_DAYS = "days"
ATTR_TIMER_REPEAT = "repeat"
ATTR_TIMER_OUTPUT = "output"
ATTR_TIMER_ACTION = "action"

CONF_DISCOVERY_TOPIC = "discovery_topic"
CONF_DEVICE_TOPICS = "device_topics"
CONF_DEVICES = "devices"

DISCOVERY_TASMOTA_CONFIG_TOPIC = "tasmota/discovery/+/config"
DISCOVERY_LWT_TOPIC = "tele/+/LWT"
DISCOVERY_STATE_TOPIC = "tele/+/STATE"
DISCOVERY_RESULT_TOPIC = "stat/+/RESULT"

ATTR_DEVICE_MAC = "mac"
ATTR_DEVICE_TOPIC = "topic"
ATTR_DEVICE_NAME = "name"

TIMER_ACTIONS = {
    0: "Off",
    1: "On",
    2: "Toggle",
    3: "Rule"
}

DAYS_OF_WEEK = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

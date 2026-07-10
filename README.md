# Tasmota Timer Configuration for Home Assistant

A Home Assistant custom component (HACS) that provides services to configure timer parameters on Tasmota devices via MQTT.

## Features

- Configure all 16 Tasmota timers with full parameter control
- Enable/disable individual timers
- Enable/disable all timers on a device at once
- Automatic discovery of Tasmota devices via MQTT
- Switch entities for each discovered device to control global timer enable state
- Query timer configurations
- Works with any Tasmota device connected via MQTT

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the `tasmota_timers` folder to your `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Tasmota Timer Configuration"
4. Click to install (no configuration parameters needed)

## Usage

This integration provides six services:

### `tasmota_timers.set_timer`

Configure a complete timer with all parameters.

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device (e.g., "tasmota_switch1")
- `timer_index` (required): Timer number (1-16)
- `enable` (optional): Enable (1) or disable (0) the timer (default: 1)
- `time` (optional): Timer time in HH:MM format (default: "00:00")
- `window` (optional): Random window in minutes 0-15 (default: 0)
- `days` (optional): Active days as 7-character string (1=active, 0=inactive, Sun-Sat) (default: "1111111")
- `repeat` (optional): Repeat daily (1) or one-time (0) (default: 1)
- `output` (optional): Output/relay number 1-8 (default: 1)
- `action` (optional): Action to perform - 0=Off, 1=On, 2=Toggle, 3=Rule (default: 1)

**Example:**
```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
  enable: 1
  time: "18:30"
  days: "0111110"  # Monday to Friday only
  action: 1  # Turn on
  output: 1
```

### `tasmota_timers.enable_timer`

Enable a specific timer.

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device
- `timer_index` (required): Timer number (1-16)

**Example:**
```yaml
service: tasmota_timers.enable_timer
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
```

### `tasmota_timers.disable_timer`

Disable a specific timer.

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device
- `timer_index` (required): Timer number (1-16)

**Example:**
```yaml
service: tasmota_timers.disable_timer
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
```

### `tasmota_timers.enable_all_timers`

Enable all timers on a Tasmota device at once.

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device

**Example:**
```yaml
service: tasmota_timers.enable_all_timers
data:
  device_topic: "tasmota_switch1"
```

### `tasmota_timers.disable_all_timers`

Disable all timers on a Tasmota device at once.

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device

**Example:**
```yaml
service: tasmota_timers.disable_all_timers
data:
  device_topic: "tasmota_switch1"
```

### `tasmota_timers.get_timers`

Request current timer configuration from a Tasmota device (results published to `stat/{device_topic}/RESULT`).

**Parameters:**
- `device_topic` (required): MQTT topic of your Tasmota device
- `timer_index` (optional): Specific timer to query (omit for all timers)

**Example:**
```yaml
service: tasmota_timers.get_timers
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
```

## Switch Entities

The integration automatically discovers Tasmota devices via MQTT and creates a switch entity for each device:

- **Entity name**: `{device_name} Timers` (or `{device_topic} Timers` for fallback/manual devices)
- **Function**: Enables or disables all timers on that device globally
- **Availability**: Tracks the device's LWT (Last Will and Testament) status
- **State**: Updated from `stat/{device_topic}/RESULT` messages

### Discovery

Devices are auto-discovered by listening to:
- `tasmota/discovery/+/config` - Tasmota native discovery config (preferred)
- `tele/+/LWT` - Online/offline status (fallback)
- `tele/+/STATE` - Device state messages (fallback)

When a Tasmota discovery config message is received, the integration uses:
- `t` from the payload as the device topic
- `dn` as the device name
- `mac` as the stable device identifier

For fallback discovery, the device topic is taken from the MQTT topic and the entity name defaults to the topic.

### Manual Device Topics

If auto-discovery is not working for some devices (for example, if LWT is disabled), you can add device topics manually:

1. Go to Settings → Devices & Services
2. Find the Tasmota Timer Configuration integration
3. Click "Configure"
4. Enter a comma-separated list of device topics, e.g.:
   ```
   tasmota_switch1,tasmota_switch2,tasmota_light
   ```

## Timer Days Format

The `days` parameter uses a 7-character string where each position represents a day:
- Position 1: Sunday
- Position 2: Monday
- Position 3: Tuesday
- Position 4: Wednesday
- Position 5: Thursday
- Position 6: Friday
- Position 7: Saturday

Examples:
- `"1111111"` - All days (default)
- `"0111110"` - Weekdays only (Mon-Fri)
- `"1000001"` - Weekends only (Sun & Sat)
- `"0101010"` - Monday, Wednesday, Friday

## Requirements

- Home Assistant with MQTT integration configured
- Tasmota devices connected via MQTT

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/m-hume/tasmota_timers).

## Licence

MIT Licence

# Tasmota Timer Configuration

Configure and manage Tasmota device timers directly from Home Assistant.

## What This Integration Does

This custom component adds powerful timer management services for your Tasmota devices, allowing you to:

- **Configure all timer parameters** - Set time, days, actions, outputs, and more
- **Enable/disable individual timers** - Toggle timers on and off without losing configuration
- **Enable/disable all timers** - Turn all device timers on or off at once
- **Switch entities** - Auto-discovered switches for each device to control global timer enable state
- **Query timer status** - Retrieve current timer settings from devices
- **Manage all 16 timers** - Full access to all available Tasmota timer slots

## Key Features

✅ **Full Timer Control** - Access all Tasmota timer parameters through Home Assistant services  
✅ **MQTT Based** - Reliable communication using your existing MQTT setup  
✅ **Native Tasmota Discovery** - Uses `tasmota/discovery/+/config` messages  
✅ **Easy to Use** - Simple service calls with clear parameter names  
✅ **No Cloud Required** - Everything runs locally  
✅ **Automation Ready** - Integrate with automations, scripts, and blueprints  

## Quick Start

After installation:

1. Add the integration via Settings → Devices & Services
2. Use the new services in Developer Tools → Services, or control timers via the auto-discovered switch entities:
   - `tasmota_timers.set_timer` - Configure a complete timer
   - `tasmota_timers.enable_timer` - Enable a timer
   - `tasmota_timers.disable_timer` - Disable a timer
   - `tasmota_timers.enable_all_timers` - Enable all timers on a device
   - `tasmota_timers.disable_all_timers` - Disable all timers on a device
   - `tasmota_timers.get_timers` - Query timer configuration
   - Switch entities `{device_name} Timers` - Toggle all timers on/off per device

## Example Usage

Set a weekday morning timer:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_bedroom_light"
  timer_index: 1
  time: "06:30"
  days: "0111110"  # Monday-Friday
  action: 1  # Turn on
```

## Requirements

- Home Assistant 2023.1.0 or later
- MQTT integration configured
- Tasmota devices connected via MQTT

## Documentation

- [Full README](https://github.com/m-hume/tasmota_timers/blob/main/README.md)
- [Installation Guide](https://github.com/m-hume/tasmota_timers/blob/main/INSTALLATION.md)
- [Usage Examples](https://github.com/m-hume/tasmota_timers/blob/main/EXAMPLES.md)

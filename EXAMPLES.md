# Usage Examples

This document provides practical examples of using the Tasmota Timer Configuration integration.

## Basic Examples

### Example 1: Simple On/Off Timer

Turn on a light every day at 6:30 PM:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_bedroom_light"
  timer_index: 1
  time: "18:30"
  action: 1  # On
  output: 1
```

Turn it off at 11:00 PM:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_bedroom_light"
  timer_index: 2
  time: "23:00"
  action: 0  # Off
  output: 1
```

### Example 2: Weekday-Only Timer

Turn on office lights Monday to Friday at 8:00 AM:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_office_light"
  timer_index: 1
  time: "08:00"
  days: "0111110"  # Mon-Fri only
  action: 1
  output: 1
```

### Example 3: Weekend Timer

Different schedule for weekends:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_living_room"
  timer_index: 3
  time: "09:00"
  days: "1000001"  # Sat & Sun only
  action: 1
  output: 1
```

### Example 4: Random Window Timer

Add randomness to simulate presence (±15 minutes):

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_entrance_light"
  timer_index: 1
  time: "19:00"
  window: 15  # Random between 18:45 and 19:15
  action: 1
  output: 1
```

### Example 5: Toggle Action

Toggle a device state:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_pump"
  timer_index: 1
  time: "06:00"
  action: 2  # Toggle
  output: 1
```

### Example 5b: Rule Action

Trigger a Tasmota rule:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_sensor"
  timer_index: 4
  time: "00:00"
  days: "1111111"
  action: 3  # Rule
  output: 1
```

## Advanced Examples

### Example 6: Multiple Outputs

Control different relays on the same device:

```yaml
# Timer 1: First relay on at 6:00
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_multi_relay"
  timer_index: 1
  time: "06:00"
  action: 1
  output: 1

# Timer 2: Second relay on at 7:00
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_multi_relay"
  timer_index: 2
  time: "07:00"
  action: 1
  output: 2
```

### Example 7: One-Time Timer

Set a timer that runs once and doesn't repeat:

```yaml
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_heater"
  timer_index: 5
  time: "22:00"
  repeat: 0  # One-time only
  action: 0
  output: 1
```

### Example 8: Automation Integration

Use in Home Assistant automations:

```yaml
automation:
  - alias: "Set Garden Lights Timer"
    trigger:
      - platform: sun
        event: sunset
        offset: "-00:30:00"
    action:
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_garden"
          timer_index: 1
          time: "{{ (now() + timedelta(minutes=30)).strftime('%H:%M') }}"
          action: 1
          output: 1
```

### Example 9: Seasonal Timers

Use scripts to set different timer schedules:

```yaml
script:
  summer_schedule:
    sequence:
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_porch"
          timer_index: 1
          time: "21:00"
          action: 1
          
  winter_schedule:
    sequence:
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_porch"
          timer_index: 1
          time: "17:00"
          action: 1
```

### Example 10: Query and Log Timers

Get current timer configuration:

```yaml
service: tasmota_timers.get_timers
data:
  device_topic: "tasmota_switch1"
```

Listen to the MQTT response at `stat/tasmota_switch1/RESULT` to see current settings.

## Management Examples

### Enable a Timer

```yaml
service: tasmota_timers.enable_timer
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
```

### Disable a Timer

```yaml
service: tasmota_timers.disable_timer
data:
  device_topic: "tasmota_switch1"
  timer_index: 1
```

### Enable All Timers on a Device

```yaml
service: tasmota_timers.enable_all_timers
data:
  device_topic: "tasmota_switch1"
```

### Disable All Timers on a Device

Useful for maintenance or temporary override:

```yaml
service: tasmota_timers.disable_all_timers
data:
  device_topic: "tasmota_switch1"
```

### Toggle All Timers via Switch Entity

Use the auto-discovered switch entity in automations:

```yaml
automation:
  - alias: "Disable all timers when away"
    trigger:
      - platform: state
        entity_id: person.jon
        to: "not_home"
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.tasmota_switch1_timers
```

The switch entity name will be `{device_topic} Timers`, e.g. `switch.tasmota_switch1_timers`.

### Bulk Timer Configuration

Configure multiple timers for a daily schedule:

```yaml
script:
  configure_daily_schedule:
    sequence:
      # Morning on
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_kitchen"
          timer_index: 1
          time: "06:30"
          days: "0111110"
          action: 1
          
      # Morning off
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_kitchen"
          timer_index: 2
          time: "08:00"
          days: "0111110"
          action: 0
          
      # Evening on
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_kitchen"
          timer_index: 3
          time: "18:00"
          action: 1
          
      # Night off
      - service: tasmota_timers.set_timer
        data:
          device_topic: "tasmota_kitchen"
          timer_index: 4
          time: "23:00"
          action: 0
```

## Tips and Best Practices

1. **Use descriptive timer indices**: Document which timer number corresponds to which schedule
2. **Test with get_timers**: Always verify your timer configuration after setting
3. **Plan timer slots**: With 16 available timers per device, plan your usage carefully
4. **Combine with automations**: Use HA automations to dynamically adjust timers based on conditions
5. **Monitor MQTT topics**: Subscribe to `stat/{device}/RESULT` to see timer confirmations
6. **Use window for security**: Random windows make presence simulation more realistic
7. **Backup configurations**: Save your timer configurations in scripts for easy recovery

## Troubleshooting Examples

### Verify Timer Setting

After setting a timer, query it to verify:

```yaml
# Set timer
service: tasmota_timers.set_timer
data:
  device_topic: "tasmota_test"
  timer_index: 1
  time: "12:00"
  action: 1

# Then verify
service: tasmota_timers.get_timers
data:
  device_topic: "tasmota_test"
  timer_index: 1
```

### Debug MQTT Communication

Enable MQTT logging in Home Assistant configuration:

```yaml
logger:
  default: info
  logs:
    custom_components.tasmota_timers: debug
    homeassistant.components.mqtt: debug
```

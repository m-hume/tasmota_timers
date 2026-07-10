# Installation Guide

## Method 1: Install via HACS (Recommended)

1. Ensure you have [HACS](https://hacs.xyz/) installed in your Home Assistant instance
2. In Home Assistant, go to HACS → Integrations
3. Click the three-dot menu (⋮) in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Add"
7. Find "Tasmota Timer Configuration" in the integrations list
8. Click "Download"
9. Restart Home Assistant
10. Go to Settings → Devices & Services → Add Integration
11. Search for "Tasmota Timer Configuration" and add it

## Method 2: Manual Installation

### For Home Assistant OS / Supervised

1. Copy the `tasmota_timers` folder to your Home Assistant's `custom_components` directory:
   ```
   /config/custom_components/tasmota_timers/
   ```

2. The structure should look like:
   ```
   /config/custom_components/tasmota_timers/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── manifest.json
   ├── services.yaml
   ├── strings.json
   └── translations/
       └── en.json
   ```

3. Restart Home Assistant

4. Go to Settings → Devices & Services → Add Integration

5. Search for "Tasmota Timer Configuration" and add it

### For Home Assistant Container

1. Mount or copy the `tasmota_timers` folder to your `custom_components` directory

2. Restart the Home Assistant container

3. Add the integration via the UI

## Verification

After installation and restart:

1. Check the Home Assistant logs for any errors related to `tasmota_timers`

2. Go to Developer Tools → Services

3. You should see six services:
   - `tasmota_timers.set_timer`
   - `tasmota_timers.enable_timer`
   - `tasmota_timers.disable_timer`
   - `tasmota_timers.enable_all_timers`
   - `tasmota_timers.disable_all_timers`
   - `tasmota_timers.get_timers`

## Prerequisites

- Home Assistant 2023.1.0 or later
- MQTT integration configured and working
- Tasmota devices connected via MQTT

## Troubleshooting

### Integration doesn't appear

- Ensure all files are in the correct location
- Check file permissions
- Verify Home Assistant was fully restarted (not just reloaded)
- Check logs for Python syntax errors

### Services not working

- Ensure MQTT integration is properly configured
- Verify your Tasmota device topics are correct
- Check that Tasmota devices are online and responding to MQTT commands
- Enable debug logging:
  ```yaml
  logger:
    default: info
    logs:
      custom_components.tasmota_timers: debug
  ```

### Timer commands not executing

- Verify the MQTT topic matches your Tasmota device configuration
- Test MQTT connectivity with a simple command like `Power` or `Status`
- Check Tasmota device logs for received commands

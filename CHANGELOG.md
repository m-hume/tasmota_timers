# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-10

### Added
- Switch platform with auto-discovered entities for each Tasmota device
- `timers_enabled` switch per device to control global timer enable state
- Native Tasmota discovery via `tasmota/discovery/+/config` messages
- Fallback MQTT device discovery via `tele/+/LWT` and `tele/+/STATE` topics
- Manual device topic configuration in options flow
- Device info from discovery payload (name, MAC, topic)

## [0.1.1] - 2026-07-10

### Added
- Service `enable_all_timers` to enable all timers on a device at once
- Service `disable_all_timers` to disable all timers on a device at once

### Changed
- Timer action `3` now labelled "Rule" instead of "Blink" to match Tasmota timer actions

## [0.1.0] - 2026-07-10

### Added
- Initial release of Tasmota Timer Configuration integration
- Service `set_timer` for full timer configuration
- Service `enable_timer` to enable specific timers
- Service `disable_timer` to disable specific timers
- Service `get_timers` to query timer configurations
- Support for all 16 Tasmota timer slots
- Full parameter control (time, days, window, action, output, repeat)
- Config flow for easy integration setup
- HACS compatibility
- Comprehensive documentation and examples

### Features
- MQTT-based communication with Tasmota devices
- Support for timer randomisation (window parameter)
- Day-of-week scheduling
- Multiple output/relay control
- Four action types (Off, On, Toggle, Rule)
- Repeating and one-time timers

## [Unreleased]

### Planned Features
- Sensor entities to display current timer status
- Timer templates/presets
- Bulk timer operations
- Visual timer editor panel
- Timer import/export functionality
- Integration with Home Assistant energy dashboard

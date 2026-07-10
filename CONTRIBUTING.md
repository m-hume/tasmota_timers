# Contributing to Tasmota Timer Configuration

Thank you for your interest in contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/m-hume/tasmota_timers/issues) section
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the issue
   - Expected vs actual behaviour
   - Home Assistant version
   - Tasmota firmware version
   - Relevant logs (enable debug logging)

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Create a new issue describing:
   - The enhancement you'd like to see
   - Why it would be useful
   - Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Create a Pull Request

## Development Setup

### Prerequisites

- Python 3.11 or later
- Home Assistant development environment
- MQTT broker (Mosquitto recommended)
- Tasmota device(s) for testing

### Setting Up Development Environment

1. Clone the repository
2. Create a symbolic link from your Home Assistant `custom_components` directory:
   ```bash
   ln -s /path/to/tasmota_timers/custom_components/tasmota_timers /path/to/homeassistant/custom_components/tasmota_timers
   ```
3. Restart Home Assistant in development mode

### Testing

Before submitting a PR, ensure:

1. All services work as expected
2. No errors in Home Assistant logs
3. Code follows Home Assistant style guidelines
4. MQTT communication is reliable
5. Error handling is appropriate

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep lines under 100 characters
- Use meaningful variable names

### Debug Logging

Enable debug logging in `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.tasmota_timers: debug
```

## What We're Looking For

- Bug fixes
- Performance improvements
- Additional timer-related features
- Better error handling
- Documentation improvements
- Translation contributions
- UI/UX enhancements

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the community

## Questions?

Feel free to open an issue for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

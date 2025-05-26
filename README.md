# mopad

An anywidget that allows gamepad input in Marimo notebooks. Perfect for interactive data exploration, games, or any application that needs real-time gamepad input.

## Features

- 🎮 **Automatic gamepad detection** - No need to press buttons before starting
- 📊 **Real-time visual feedback** - Connection status and button press information  
- ⏱️ **Precise timestamp tracking** - Millisecond-accurate timing for button presses
- 🔗 **Any button support** - Capture input from any bluetooth gamepad

## Installation

```bash
pip install mopad
```

## Usage

### Basic Example

```python
import marimo as mo
from mopad import MopadWidget

# Create and display the widget
gamepad = mo.ui.anywidget(MopadWidget())
gamepad
```

For a full demo you can check [Github pages](https://koaning.github.io/mopad/).

## Widget Properties

| Property | Type | Description |
|----------|------|-------------|
| `last_button_pressed` | `int` | Index of the last pressed button (-1 if none) |
| `current_timestamp` | `float` | Timestamp of the most recent button press (ms) |
| `previous_timestamp` | `float` | Timestamp of the previous button press (ms) |
| `axes` | `list[float]` | Analog stick values: [left_x, left_y, right_x, right_y] |
| `dpad_up` | `bool` | True when D-pad up is pressed |
| `dpad_down` | `bool` | True when D-pad down is pressed |
| `dpad_left` | `bool` | True when D-pad left is pressed |
| `dpad_right` | `bool` | True when D-pad right is pressed |
| `button_id` | `int` | Legacy property for backward compatibility |
k
## Gamepad Setup

1. **Connect your gamepad** to your computer (USB or Bluetooth)
2. **Press any button** on the gamepad to activate it in the browser
3. **Start the widget** - it will automatically detect the connected gamepad

> **Note:** Due to browser security policies, gamepads need user interaction to be detected. The widget will guide you through the connection process with clear visual indicators.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
# mopad

[![CI](https://github.com/vincentwarmerdam/mopad/actions/workflows/ci.yml/badge.svg)](https://github.com/vincentwarmerdam/mopad/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/mopad.svg)](https://badge.fury.io/py/mopad)

An anywidget that allows gamepad input in Marimo notebooks. Perfect for interactive data exploration, games, or any application that needs real-time gamepad input.

## Features

- 🎮 **Automatic gamepad detection** - No need to press buttons before starting
- 📊 **Real-time visual feedback** - Connection status and button press information  
- ⏱️ **Precise timestamp tracking** - Millisecond-accurate timing for button presses
- 🔗 **Any button support** - Capture input from any gamepad button
- 🔧 **Minimizable interface** - Hide the widget when you don't need the UI
- 🚀 **Zero setup** - Works out of the box in Marimo

## Installation

```bash
pip install mopad
```

## Quick Start

```python
import marimo as mo
from mopad import MopadWidget

# Display it in your notebook
gamepad = mo.ui.anywidget(MopadWidget())
gamepad
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

### Accessing Button Data

The widget provides three key properties:

```python
# Which button was pressed last (0, 1, 2, 3, ...)
print(f"Last button: {gamepad.value.last_button_pressed}")

# When it was pressed (milliseconds since epoch)
print(f"Current timestamp: {gamepad.value.current_timestamp}")
print(f"Previous timestamp: {gamepad.value.previous_timestamp}")

# Calculate time between button presses
if gamepad.value.previous_timestamp > 0:
    time_diff = (gamepad.value.current_timestamp - gamepad.value.previous_timestamp) / 1000
    print(f"Time between presses: {time_diff:.3f} seconds")
```

### Interactive Example

```python
import marimo as mo
from mopad import MopadWidget
import datetime

gamepad = mo.ui.anywidget(MopadWidget())

# React to button presses
if gamepad.value.last_button_pressed >= 0:
    button = gamepad.value.last_button_pressed
    timestamp = datetime.datetime.fromtimestamp(gamepad.value.current_timestamp / 1000)
    
    mo.md(f"""
    ## Last Input
    - **Button:** {button}
    - **Time:** {timestamp.strftime('%H:%M:%S.%f')[:-3]}
    - **Action:** {['Jump', 'Attack', 'Defend', 'Special'][button] if button < 4 else f'Button {button}'}
    """)
else:
    mo.md("Press any button on your gamepad!")
```

## Widget Properties

| Property | Type | Description |
|----------|------|-------------|
| `last_button_pressed` | `int` | Index of the last pressed button (-1 if none) |
| `current_timestamp` | `float` | Timestamp of the most recent button press (ms) |
| `previous_timestamp` | `float` | Timestamp of the previous button press (ms) |
| `button_id` | `int` | Legacy property for backward compatibility |

## Gamepad Setup

1. **Connect your gamepad** to your computer (USB or Bluetooth)
2. **Press any button** on the gamepad to activate it in the browser
3. **Start the widget** - it will automatically detect the connected gamepad

> **Note:** Due to browser security policies, gamepads need user interaction to be detected. The widget will guide you through the connection process with clear visual indicators.

## Widget Interface

The widget provides a clean, informative interface:

- **🟢 Connected status** - Shows when gamepad is detected with device name
- **🔴 Disconnected status** - Provides connection instructions  
- **📝 Button feedback** - Displays which button was pressed
- **⏱️ Timestamp display** - Shows current, previous, and time difference
- **➖/➕ Minimize button** - Hide/show the full interface

## Use Cases

- **Interactive data visualization** - Navigate through datasets with gamepad controls
- **Real-time monitoring** - Use buttons to trigger actions or mark events
- **Game development** - Prototype games directly in notebooks
- **Accessibility** - Alternative input method for users who prefer gamepads
- **Timing experiments** - Precise measurement of reaction times

## Examples

### Rhythm Game Timer
```python
import marimo as mo
from mopad import MopadWidget

gamepad = mo.ui.anywidget(MopadWidget())

# Check timing accuracy
if gamepad.value.previous_timestamp > 0:
    beat_interval = (gamepad.value.current_timestamp - gamepad.value.previous_timestamp) / 1000
    target_bpm = 120  # Target: 120 BPM = 0.5s per beat
    target_interval = 60 / target_bpm
    accuracy = abs(beat_interval - target_interval)
    
    if accuracy < 0.05:  # Within 50ms
        mo.md("🎯 **Perfect timing!**")
    elif accuracy < 0.1:  # Within 100ms  
        mo.md("👍 **Good timing!**")
    else:
        mo.md("⚠️ **Try to keep the beat!**")
```

### Button Mapping
```python
button_actions = {
    0: "🔥 Fire primary weapon",
    1: "🛡️ Activate shield", 
    2: "⚡ Use special ability",
    3: "🏃 Sprint mode"
}

if gamepad.value.last_button_pressed in button_actions:
    action = button_actions[gamepad.value.last_button_pressed]
    mo.md(f"**Action triggered:** {action}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
import traitlets
import anywidget


class MopadWidget(anywidget.AnyWidget):
    """
    An anywidget that allows gamepad input in Marimo.
    
    This widget automatically detects gamepad connection and provides
    visual feedback about the connection status.
    """
    
    _esm = """
    function render({model, el}){
        let lastButtonPressed = model.get("last_button_pressed");
        let currentTimestamp = model.get("current_timestamp");
        let previousTimestamp = model.get("previous_timestamp");
        let axes = model.get("axes");
        let dpadUp = model.get("dpad_up");
        let dpadDown = model.get("dpad_down");
        let dpadLeft = model.get("dpad_left");
        let dpadRight = model.get("dpad_right");
        let isMinimized = false;
        
        // Create UI elements
        const container = document.createElement("div");
        container.style.cssText = `
            font-family: system-ui, -apple-system, sans-serif;
            padding: 16px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            background: #f9fafb;
            max-width: 400px;
            transition: all 0.3s ease;
        `;
        
        const header = document.createElement("div");
        header.style.cssText = "display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;";
        
        const title = document.createElement("h3");
        title.textContent = "🎮 Mopad Widget";
        title.style.cssText = "margin: 0; color: #374151;";
        
        const toggleButton = document.createElement("button");
        toggleButton.textContent = "−";
        toggleButton.style.cssText = `
            background: #6b7280;
            color: white;
            border: none;
            border-radius: 4px;
            width: 24px;
            height: 24px;
            cursor: pointer;
            font-size: 16px;
            line-height: 1;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        toggleButton.onmouseover = () => toggleButton.style.background = "#4b5563";
        toggleButton.onmouseout = () => toggleButton.style.background = "#6b7280";
        
        const content = document.createElement("div");
        
        const status = document.createElement("div");
        status.style.cssText = `
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 12px;
            font-weight: 500;
        `;
        
        const instructions = document.createElement("div");
        instructions.style.cssText = "font-size: 14px; color: #6b7280; margin-bottom: 12px;";
        
        const timestampDisplay = document.createElement("div");
        timestampDisplay.style.cssText = `
            font-size: 14px;
            color: #374151;
            padding: 4px 0;
            font-family: monospace;
        `;
        
        const buttonDisplay = document.createElement("div");
        buttonDisplay.style.cssText = `
            font-size: 16px;
            color: #374151;
            padding: 4px 0;
        `;
        
        const dpadDisplay = document.createElement("div");
        dpadDisplay.style.cssText = `
            font-size: 14px;
            color: #374151;
            padding: 4px 0;
            font-family: monospace;
        `;
        
        const axesDisplay = document.createElement("div");
        axesDisplay.style.cssText = `
            font-size: 14px;
            color: #374151;
            padding: 4px 0;
            font-family: monospace;
        `;
        
        header.appendChild(title);
        header.appendChild(toggleButton);
        content.appendChild(status);
        content.appendChild(instructions);
        content.appendChild(buttonDisplay);
        content.appendChild(dpadDisplay);
        content.appendChild(axesDisplay);
        content.appendChild(timestampDisplay);
        container.appendChild(header);
        container.appendChild(content);
        el.appendChild(container);
        
        // Toggle minimize/expand
        toggleButton.addEventListener("click", () => {
            isMinimized = !isMinimized;
            if (isMinimized) {
                content.style.display = "none";
                container.style.padding = "8px 16px";
                toggleButton.textContent = "+";
            } else {
                content.style.display = "block";
                container.style.padding = "16px";
                toggleButton.textContent = "−";
            }
        });

        const frames = window.mozRequestAnimationFrame || window.requestAnimationFrame;
        let gamepadConnected = false;
        let lastGamepadState = null;
        
        function updateStatus(connected, gamepad = null) {
            if (connected) {
                status.style.cssText += "background: #dcfce7; color: #166534; border: 1px solid #bbf7d0;";
                status.textContent = `✅ Gamepad Connected: ${gamepad?.id || 'Unknown'}`;
                instructions.textContent = `Press any button on the gamepad to interact.`;
                gamepadConnected = true;
            } else {
                status.style.cssText += "background: #fef2f2; color: #dc2626; border: 1px solid #fecaca;";
                status.textContent = "❌ No Gamepad Detected";
                instructions.innerHTML = `
                    To connect your gamepad:<br>
                    1. Connect your gamepad to your computer<br>
                    2. Press any button on the gamepad<br>
                    3. The widget will automatically detect it
                `;
                gamepadConnected = false;
            }
        }
        
        function updateButtonDisplay() {
            if (lastButtonPressed >= 0) {
                buttonDisplay.textContent = `Last button pressed: ${lastButtonPressed}`;
            } else {
                buttonDisplay.textContent = "No button pressed yet";
            }
        }
        
        function updateDpadDisplay() {
            const directions = [];
            if (dpadUp) directions.push("↑");
            if (dpadDown) directions.push("↓"); 
            if (dpadLeft) directions.push("←");
            if (dpadRight) directions.push("→");
            
            dpadDisplay.textContent = directions.length > 0 
                ? `D-pad: ${directions.join(" ")}` 
                : "D-pad: —";
        }
        
        function updateAxesDisplay() {
            if (axes && axes.length >= 4) {
                const [leftX, leftY, rightX, rightY] = axes;
                axesDisplay.innerHTML = `
                    Left stick: (${leftX.toFixed(2)}, ${leftY.toFixed(2)})<br>
                    Right stick: (${rightX.toFixed(2)}, ${rightY.toFixed(2)})
                `;
            } else {
                axesDisplay.textContent = "Sticks: No data";
            }
        }
        
        function updateTimestampDisplay() {
            if (currentTimestamp > 0) {
                const current = new Date(currentTimestamp).toLocaleTimeString();
                const previous = previousTimestamp > 0 ? new Date(previousTimestamp).toLocaleTimeString() : "None";
                const timeDiff = previousTimestamp > 0 ? ((currentTimestamp - previousTimestamp) / 1000).toFixed(3) : "N/A";
                timestampDisplay.innerHTML = `
                    Current: ${current}<br>
                    Previous: ${previous}<br>
                    Time diff: ${timeDiff}s
                `;
            } else {
                timestampDisplay.textContent = "No button presses recorded";
            }
        }
        
        function checkGamepadConnection() {
            const gamepads = navigator.getGamepads();
            const gamepad = gamepads[0] || gamepads[1] || gamepads[2] || gamepads[3];
            
            if (gamepad && gamepad.connected) {
                if (!gamepadConnected) {
                    updateStatus(true, gamepad);
                }
                return gamepad;
            } else {
                if (gamepadConnected) {
                    updateStatus(false);
                }
                return null;
            }
        }
        
        function run_loop(){
            const gamepad = checkGamepadConnection();
            
            if (gamepad && gamepadConnected) {
                let buttonPressed = false;
                const currentState = gamepad.buttons.map(b => b.pressed).join('');
                
                // Check if any button state changed
                if (currentState !== lastGamepadState) {
                    gamepad.buttons.forEach((button, i) => {
                        if (button.pressed) {
                            // A button was pressed, update timestamps
                            previousTimestamp = currentTimestamp;
                            currentTimestamp = Date.now();
                            lastButtonPressed = i;
                            
                            model.set("last_button_pressed", lastButtonPressed);
                            model.set("current_timestamp", currentTimestamp);
                            model.set("previous_timestamp", previousTimestamp);
                            model.save_changes();
                            
                            updateButtonDisplay();
                            updateTimestampDisplay();
                            buttonPressed = true;
                        }
                    });
                }
                
                // Update axes (analog sticks) - always update these
                if (gamepad.axes && gamepad.axes.length >= 4) {
                    const newAxes = [
                        gamepad.axes[0] || 0,  // Left stick X
                        gamepad.axes[1] || 0,  // Left stick Y  
                        gamepad.axes[2] || 0,  // Right stick X
                        gamepad.axes[3] || 0   // Right stick Y
                    ];
                    
                    // Only update if values changed significantly (avoid noise)
                    const threshold = 0.05;
                    let axesChanged = false;
                    for (let i = 0; i < 4; i++) {
                        if (Math.abs(newAxes[i] - axes[i]) > threshold) {
                            axesChanged = true;
                            break;
                        }
                    }
                    
                    if (axesChanged) {
                        axes = newAxes;
                        model.set("axes", axes);
                        model.save_changes();
                        updateAxesDisplay();
                    }
                }
                
                // Update D-pad (usually buttons 12-15 on standard gamepads)
                const newDpadUp = gamepad.buttons[12] ? gamepad.buttons[12].pressed : false;
                const newDpadDown = gamepad.buttons[13] ? gamepad.buttons[13].pressed : false;
                const newDpadLeft = gamepad.buttons[14] ? gamepad.buttons[14].pressed : false;
                const newDpadRight = gamepad.buttons[15] ? gamepad.buttons[15].pressed : false;
                
                if (newDpadUp !== dpadUp || newDpadDown !== dpadDown || 
                    newDpadLeft !== dpadLeft || newDpadRight !== dpadRight) {
                    dpadUp = newDpadUp;
                    dpadDown = newDpadDown;
                    dpadLeft = newDpadLeft;
                    dpadRight = newDpadRight;
                    
                    model.set("dpad_up", dpadUp);
                    model.set("dpad_down", dpadDown);
                    model.set("dpad_left", dpadLeft);
                    model.set("dpad_right", dpadRight);
                    model.save_changes();
                    updateDpadDisplay();
                }
                
                lastGamepadState = currentState;
                
                // Slower polling when button is pressed to prevent rapid firing
                setTimeout(() => frames(run_loop), buttonPressed ? 200 : 50);
            } else {
                // Check for gamepad connection more frequently when disconnected
                setTimeout(() => frames(run_loop), 100);
            }
        }
        
        // Listen for gamepad connection events
        window.addEventListener("gamepadconnected", (e) => {
            updateStatus(true, e.gamepad);
        });
        
        window.addEventListener("gamepaddisconnected", (e) => {
            updateStatus(false);
        });
        
        // Initial setup
        updateStatus(false);
        updateButtonDisplay();
        updateDpadDisplay();
        updateAxesDisplay();
        updateTimestampDisplay();
        
        // Watch for changes from Python side
        model.on("change:last_button_pressed", () => {
            lastButtonPressed = model.get("last_button_pressed");
            updateButtonDisplay();
        });
        
        model.on("change:current_timestamp", () => {
            currentTimestamp = model.get("current_timestamp");
            updateTimestampDisplay();
        });
        
        model.on("change:previous_timestamp", () => {
            previousTimestamp = model.get("previous_timestamp");
            updateTimestampDisplay();
        });
        
        model.on("change:axes", () => {
            axes = model.get("axes");
            updateAxesDisplay();
        });
        
        model.on("change:dpad_up change:dpad_down change:dpad_left change:dpad_right", () => {
            dpadUp = model.get("dpad_up");
            dpadDown = model.get("dpad_down");
            dpadLeft = model.get("dpad_left");
            dpadRight = model.get("dpad_right");
            updateDpadDisplay();
        });
        
        run_loop();
    };

    export default { render };
    """
    
    last_button_pressed = traitlets.Int(-1).tag(sync=True)
    current_timestamp = traitlets.Float(0.0).tag(sync=True)
    previous_timestamp = traitlets.Float(0.0).tag(sync=True)
    
    # Dpad and analog stick values (axes[0-3] are typically: left_x, left_y, right_x, right_y)
    axes = traitlets.List(trait=traitlets.Float(), default_value=[0.0, 0.0, 0.0, 0.0]).tag(sync=True)
    dpad_up = traitlets.Bool(False).tag(sync=True)
    dpad_down = traitlets.Bool(False).tag(sync=True)
    dpad_left = traitlets.Bool(False).tag(sync=True)
    dpad_right = traitlets.Bool(False).tag(sync=True)
    
    button_id = traitlets.Int(0).tag(sync=True)  # Kept for backward compatibility
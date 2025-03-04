# mopad

An anywidget that allows gamepad input in Marimo

> There is an annoying thing with this API and that is that you need to hit a few buttons to actually connect the gamepad to the browser *before* starting this widget. Just be mindful of that. 

```python
import traitlets
import anywidget

class MopadWidget(anywidget.AnyWidget):
    _esm = """
    function render({model, el}){
        const btnId = model.get("button_id");
        let value = model.get("value");
        let p = document.createElement("p");
        p.innerHTML = 'mopad'
        el.appendChild(p)

        const frames = window.mozRequestAnimationFrame || window.requestAnimationFrame; 
        
        function run_loop(){
            const gamepad = navigator.getGamepads()[0];
            let wait = false;
            gamepad.buttons.map(function(d, i){
                if(d.pressed){
                    if(i == btnId){
                        // Select the previous sentence
                        value = value + 1; 
                        model.set("value", value);
                        model.save_changes();
                        p.innerHTML = `update: ${value}`
                        wait = true;
                    }
                }
            })
            if(wait){
                setTimeout(() => frames(run_loop), 200)
                wait = false;
            }else{
                setTimeout(() => frames(run_loop), 50)
            }
        }
        
        run_loop()
    };

    export default { render };
    """
    value = traitlets.Int(0).tag(sync=True)
    button_id = traitlets.Int(0).tag(sync=True)
```

// Sketches are boxes which the user can output text and pictures to

var last_callback_time = 0;

function create_sketch(canvas_id){
    let sketch = {
        guid: eel.guid() + ' ' + canvas_id,

        canvas: document.getElementById(canvas_id),

        commands: [[1, [0, 100, 0]], [2, [10, 10, 100, 200]]],

        waiting: false,

        redraw: true,

        draw: function(){
            if(!sketch.waiting){
                sketch.waiting = true;
                sketch.update_sketch();

                if(sketch.redraw){
                    draw_sketch(sketch.canvas, sketch.commands);
                }
            }
            requestAnimationFrame(sketch.draw);
        },

        geometry: function(){
            let b = sketch.canvas.getBoundingClientRect();
            let title_bar = window.outerHeight - window.innerHeight;
            b.x += window.screenX + window.scrollX;
            b.y += window.screenY + window.scrollY + title_bar;
            return [b.x, b.y, b.width, b.height];
        },

        update_sketch: function(){
            eel.draw_frame(sketch.guid, sketch.geometry())(
                function(commands){
                    sketch.commands = commands;
                    sketch.waiting = false;
                }
            );  
        },

        on_wheel: function(evt) {
            evt.preventDefault();
            if (!evt){
                evt = event;
            }
            var direction = (evt.detail < 0 || evt.wheelDelta > 0) ? 1 : -1;
            if(Date.now() - last_callback_time > 100) {
                // Only fire this event every 100ms (cross-platform homogenising)
                eel.sketch_wheel(sketch.guid, direction);
                last_callback_time = Date.now();
            }
        },

        on_click: function(evt) {
            let b = sketch.canvas.getBoundingClientRect();
            eel.sketch_click(sketch.guid, evt.clientX - b.left, evt.clientY - b.top);
        },
    }
    
    // Mouse listeners
    sketch.canvas.addEventListener('DOMMouseScroll', sketch.on_wheel, false);
    sketch.canvas.addEventListener('mousewheel', sketch.on_wheel, false);
    sketch.canvas.addEventListener('wheel', sketch.on_wheel, false);
    sketch.canvas.addEventListener('mousedown', sketch.on_click, false);

    // Start paint loop
    sketch.draw();

    return sketch;
}

function draw_sketch(canvas, commands){
    let context = canvas.getContext('2d');

    for(let i = 0; i < commands.length; i++) {
        let c = commands[i][0]
        let args = commands[i][1];

        switch(c){
            case DRAW_CLEAR:
                context.clearRect(0, 0, canvas.width, canvas.height);
                break;
            case DRAW_INK:
                let r = args[0], g = args[1], b = args[2];
                context.fillStyle = `rgb(${r}, ${g}, ${b})`;
                context.strokeStyle = context.fillStyle;
                break;
            case DRAW_RECT:
                context.fillRect(args[0], args[1], args[2], args[3]);
                break;
            case DRAW_STROKE:
                context.beginPath();
                context.moveTo(args[0], args[1]);
                context.lineTo(args[2], args[3]);
                context.closePath();
                context.stroke();
                break;
            case DRAW_CIRC:
                context.beginPath();
                context.arc(args[0], args[1], args[2], 0, 2 * Math.PI);
                context.fill();
                context.stroke();
                break;
            case DRAW_TEXT:
                context.font = `${args[3]}px Arial`;
                context.fillText(args[2], args[0], args[1]);
        }
    }
}




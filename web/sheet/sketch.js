// Sketches are boxes which the user can output text and pictures to

function add_sketch_div(label, code, x, y, width, height){
    var guid = ('sketch' + Date.now() + Math.random()).replace('.', '');
    var div = $(`<div class='sketch'>
                     <div class='label' /><!--
                  --><div class='output'><canvas /><div class='text' /></div>
                 </div>`);
    div.attr('id', guid);
    div.css('left', x)
       .css('top', y);
    div.find('.label').html(label.replace(' ', '&nbsp;'));
    $('#sketches').append(div);

    let canvas = div.find('canvas').get(0);
    
    div.draggable({handle: '.label'});
    div.find('.output').resizable({ handles: 'se', autoHide: true })
                       .resize(function(e, ui){
                            canvas.height = ui.size.height + 5;
                            canvas.width = ui.size.width + 5;
                        });

    div.find('.output').height(height).width(width);
    canvas.height = height;
    canvas.width = width;

    let sketch = create_sketch(div);
    sketch.set_metacode(code);
    return div.get(0);
}

function create_sketch(div, guid=null, text=null, canvas=null){
    if(div){
        text   = text   ? text   : div.find('.text').get(0);
        canvas = canvas ? canvas : div.find('canvas').get(0);
        guid   = guid   ? guid   : eel.guid() + '::' + div.attr('id');
    }

    let sketch = {
        guid:       guid,
        text:       text,        
        canvas:     canvas,
        borders:    get_canvas_borders(canvas),
        commands:   [],
        waiting:    false,
        redraw:     true,
        animate:    true,
        last_wheel: 0,

        draw: function(){
            if(!sketch.waiting){
                sketch.waiting = true;
                sketch.refresh_sketch();

                if(sketch.redraw){
                    draw_sketch(sketch.canvas, sketch.commands);
                }
            }

            if(sketch.animate){
                requestAnimationFrame(sketch.draw);
            }
        },

        geometry: function(){
            let b = sketch.canvas.getBoundingClientRect();
            let window_trim = (window.outerWidth - window.innerWidth) / 2.0;
            let title_bar = window.outerHeight - window.innerHeight - window_trim;
            b.x += window.screenX + sketch.borders.left + window_trim; // + window.scrollX;
            b.y += window.screenY + sketch.borders.top + title_bar; // + window.scrollY 
            return [b.x, b.y, b.width, b.height];
        },

        set_metacode: function(code){
            eel.set_metacode(sketch.guid, code);
        },

        refresh_sketch: function(){
            eel.sketch_refresh(sketch.guid, sketch.geometry())(
                function(data){
                    sketch.commands = data.canvas;
                    if(sketch.text && sketch.text.textContent !== data.output){
                        sketch.text.textContent = data.output;
                    }
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
            if(Date.now() - sketch.last_wheel > 50) {
                // Only fire this event every 50ms (cross-platform homogenising)
                eel.sketch_wheel(sketch.guid, direction);
                sketch.last_wheel = Date.now();
            }
        },

        on_click: function(evt) {
            if(evt.button == 0){
                let b = sketch.canvas.getBoundingClientRect();
                eel.sketch_click(sketch.guid, evt.clientX - b.left - sketch.borders.left,
                                              evt.clientY - b.top - sketch.borders.top);
            }
        },

        delete: function(){
            sketch.animate = false;
            if(div){
                div.remove();
            }
        },

        fullscreen: function(text, canvas){
            sketch.old = {text: sketch.text, canvas: sketch.canvas};
            sketch.text = text;
            sketch.canvas = canvas;
            let context = canvas.getContext('2d');
            context.clearRect(0, 0, canvas.width, canvas.height);
        },

        restore: function(){
            sketch.text = sketch.old.text;
            sketch.canvas = sketch.old.canvas;
            sketch.old = null;
        },
    }

    if(div){
        div.get(0).sketch = sketch;
    }

    // Mouse listeners
    if(text){
        text.addEventListener('DOMMouseScroll', sketch.on_wheel, false);
        text.addEventListener('mousewheel', sketch.on_wheel, false);
        text.addEventListener('wheel', sketch.on_wheel, false);
        text.addEventListener('mousedown', sketch.on_click, false);
    }

    // Start paint loop
    sketch.draw();

    return sketch;
}

function get_canvas_borders(canvas){
    var style = window.getComputedStyle(canvas);
    var borders = {}
    $.each(['left', 'top', 'right', 'bottom'], function(i, edge){
        borders[edge] = parseInt(style.getPropertyValue('padding-' + edge)) + 
                        parseInt(style.getPropertyValue('border-' + edge));
    });
    return borders;
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
            case DRAW_LINE:
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

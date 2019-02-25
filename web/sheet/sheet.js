var electron = nodeRequire('electron');

var canvas, context;
var can_update = true;
var draw_commands = [];

function frame_update(commands){
    draw_commands = commands;
    can_update = true;
}

function draw_frame(){
    let fullscreen = true;  // TODO: this
    if(fullscreen){
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    for(let i = 0; i < draw_commands.length; i++) {
        let c = draw_commands[i][0]
        let args = draw_commands[i][1];

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

    // Ask for a new frame from Python if we haven't already
    if(can_update){
        can_update = false;
        canvas_geom = get_canvas_geometry() // (might have been resized)
        eel.draw_frame(eel.guid(), canvas_geom)(frame_update);
    }

    requestAnimationFrame(draw_frame);
}

function get_canvas_geometry(){
    let b = canvas.getBoundingClientRect();
    let title_bar = window.outerHeight - window.innerHeight;
    b.x += window.screenX + window.scrollX;
    b.y += window.screenY + window.scrollY + title_bar;
    return [b.x, b.y, b.width, b.height];
}

function update_position(x, y){
    eel.sheet_dragged(eel.guid(), x, y);
}

$(function(){
    update_position(window.screenX, window.screenY);
    canvas = $('#sheet-canvas').get(0);
    context = canvas.getContext('2d');
    context.fillStyle = 'rgb(100, 200, 0)';
    draw_frame();
});


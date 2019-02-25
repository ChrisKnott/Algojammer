var app;
var dots = [];
var guides = {};
var rulers = [];
var ruler_texts = [];
var mouse = {x: 0, y: 0};
var camera = {scale: 10, x: -10, smooth_x: -10, smooth_scale: 10};
var exception_text = new PIXI.Text('', {fontFamily: 'Courier', fontSize: 14, 
                                        fill: 0xff1010, align: 'left'});
var fetching_state = false;
var current_execution_step = 0;

function init_timeline() {
    app = new PIXI.Application({antialias: true,
                                view: $('#timeline_canvas').get(0)});
    app.renderer.backgroundColor = 0x272822;
    
    for(var i = 0; i < 11; i++){
        var ruler = new PIXI.Graphics();
        ruler.lineStyle(1.0, 0xFFFFFF, 1.0);
        ruler.moveTo(0, 0);
        ruler.lineTo(0, 20);
        ruler.lineStyle(0.5, 0x555555, 0.5);
        ruler.lineTo(0, -1000);
        var fill = i < 10 ? 0x777777 : 0xdddddd;
        var ruler_text = new PIXI.Text('', {fontFamily: 'Courier', fontSize: 10, 
                                            fill: fill, align : 'left'});
        app.stage.addChild(ruler);
        app.stage.addChild(ruler_text);
        rulers.push(ruler);
        ruler_texts.push(ruler_text);
    }

    for(var i = 0; i < 3000; i++) {
        var dot = new PIXI.Graphics();
        //dot.beginFill(Math.round(Math.random() * (1 << 24)));//3B3A32);
        dot.beginFill(0xDDDDDD);
        dot.drawRect(0, -4, 1, 8);
        dot.endFill();
        dot.x = dot.y = dot.line = 0;
        dots.push(dot);
        if(i > 0) {
            app.stage.addChild(dot);
        }
    }
    app.stage.addChild(dots[0]);

    $.each(['h', 'v'], function(i, d) {
        guides[d] = new PIXI.Graphics();
        guides[d].lineStyle(0.5, 0xDDDDDD, 0.5);
        guides[d].moveTo(0, 0);
        guides[d].lineTo(d === 'h' ? 1000 : 0, d === 'h' ? 0 : 1000);
        app.stage.addChild(guides[d]);
    });

    app.stage.addChild(exception_text);

    $('#timeline_canvas').mousemove(timeline_mouse_move);
    $('#timeline_canvas').mousedown(timeline_mouse_down);
    $('#timeline_canvas').mouseleave(timeline_mouse_end);
    $('#timeline_canvas').mouseup(timeline_mouse_end);
    add_scroll_callback(zoom_timeline, $('#timeline_canvas').get(0));
    
    animate();
}

function animate(){
    var h = $('#editor').height();
    app.renderer.resize(600, h);
    exception_text.text = '';

    camera.x = Math.min(Math.max(-30, camera.x), lines.length * camera.scale - 50);
    camera.smooth_x += (camera.x - camera.smooth_x) * 0.3;
    camera.smooth_scale += (camera.scale - camera.smooth_scale) * 0.3;

    var execution_step = Math.round((mouse.x + camera.x) / camera.scale);
    execution_step = Math.max(0, Math.min(execution_step, lines.length - 1));

    if(shift_key){
        current_execution_step = execution_step;
    }

    render_timeline(execution_step, current_execution_step);
    highlight_line(lines[current_execution_step]);
    draw_ruler(execution_step);

    update_state(current_execution_step);

    requestAnimationFrame(animate);
}

function update_state(step){
    if(!fetching_state){
        fetching_state = true;
        eel.update_state(step, false)(function(_){
            fetching_state = false;
        });
    }
}

function screen_pos(x){
    return camera.smooth_scale * x - camera.smooth_x;
}

function render_timeline(mouse_step, current_step){
    var h = editor.renderer.lineHeight;
    var m = (h / 2) + editor.renderer.scrollMargin.top;
    guides['h'].y = m + (lines[current_step] - 1) * h;
    guides['v'].x = screen_pos(mouse_step);
    $.each(dots, function(i, dot){
        dot.x = dot.y = -10;
        dot.scale.set(1, 1);
    });

    var first_step = Math.round(camera.smooth_x / camera.smooth_scale) - 1;
    first_step = Math.max(0, first_step);
    render_dots(first_step, current_step, m, h);

    dots[0].tint = (1 << 24) - 1;
    dots[0].z = -100;
    dots[0].x = screen_pos(current_step) - 6;
    dots[0].y = m + (lines[current_step] - 1) * h;
    dots[0].scale.set(12, 1.5);
    var data = lines[current_step];
    if(data && data.kind === 'exception'){
        dots[0].tint = (255 << 16);
        exception_text.text = data.detail;
        exception_text.x = dots[0].x + 10;
        exception_text.y = dots[0].y + 4;
    }
}

// Uses 'visits' array to efficiently render execution steps
function render_dots(first_step, current_step, margin, line_height) {
    var d = 1, s = 1;
    for(l = 0; l < visits.length; l++){         // Draw dots line by line
        var i = visits[l].bisect(first_step);
        var step = visits[l][i];
        while(screen_pos(step) < screen_pos(first_step) + 650){
            dots[d].x = screen_pos(step) - 4;
            dots[d].y = margin + l * line_height;
            if(step < current_step){
                dots[d].tint = (1 << 24) - 1;
            } else {
                dots[d].tint = (100 << 16) + (100 << 8) + 100;
            }

            while(true) {
                var gap = screen_pos(visits[l][i + s]) - screen_pos(visits[l][i]);
                var split = (visits[l][i] < current_step) != (visits[l][i + s] < current_step)
                if(!(gap < 8) || split) {
                    if(s == 1){
                        break;
                    } else {
                        s /= 2;
                    }
                } else {
                    i += s;
                    s *= 2;
                }
            }

            dots[d].scale.x = screen_pos(visits[l][i]) - screen_pos(step) + 8;
            step = visits[l][++i];

            if(++d >= 3000){
                return; // Ran out of dots!
            }
        }
    }
}

function draw_ruler(n){
    var step = 10, scale = 2;
    while(step < 80 / camera.smooth_scale){
        step *= scale;
        scale = scale == 2 ? 5 : 2;
    }

    var shift = step * Math.round(camera.smooth_x / (camera.smooth_scale * step));
    var h = window.innerHeight + window.pageYOffset;
    for(var i = 0; i < 10; i++){
        var s = i * step + shift;
        rulers[i].x = screen_pos(s);
        rulers[i].y = h - 20;
        ruler_texts[i].text = s.toLocaleString();
        ruler_texts[i].x = rulers[i].x + 3;
        ruler_texts[i].y = h - 20;
    }
    ruler_texts[10].text = n.toLocaleString();
    ruler_texts[10].x = guides['v'].x + 3;
    ruler_texts[10].y = h - 20;
}

// Controls =====

function timeline_mouse_move(evt){
    mouse.x = evt.offsetX;
    mouse.y = evt.offsetY;
    if(mouse.click_x){
        camera.x = camera.anchor - (mouse.x - mouse.click_x);
    }
}

function timeline_mouse_down(evt) {
    mouse.click_x = evt.offsetX;
    camera.anchor = camera.x;
}

function timeline_mouse_end(evt) {
    mouse.click_x = mouse.click_y = undefined;
}

function zoom_timeline(d) {
    var anchor = Math.round((guides['v'].x + camera.x) / camera.scale);
    new_scale = Math.min(15, 500 / lines.length);
    if(d == 1){
        new_scale = Math.min(15, camera.scale * 1.25);
    } else if(d == -1){
        new_scale = Math.max(new_scale, camera.scale / 1.25);
    }
    camera.x += anchor * (new_scale - camera.scale);
    camera.scale = new_scale;
}

function add_scroll_callback(callback, element){
    var last_callback_time = 0;
    var handle_scroll = function(evt) {
        evt.preventDefault();
        if (!evt){
            evt = event;
        }
        var direction = (evt.detail < 0 || evt.wheelDelta > 0) ? 1 : -1;
        if(Date.now() - last_callback_time > 100) {
            callback(direction);
            last_callback_time = Date.now();
        }
    };
    
    element.addEventListener('DOMMouseScroll', handle_scroll, false);
    element.addEventListener('mousewheel', handle_scroll, false);
    element.addEventListener('wheel', handle_scroll, false);
}

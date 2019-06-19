// FPS
//(function(){var script=document.createElement('script');script.onload=function(){var stats=new Stats();document.body.appendChild(stats.dom);requestAnimationFrame(function loop(){stats.update();requestAnimationFrame(loop)});};script.src='//rawgit.com/mrdoob/stats.js/master/build/stats.min.js';document.head.appendChild(script);})();
//============================================================================================================

var editor, back_sketch, front_sketch;

const edit_canvas_menu = new Menu();
add_menu_item(edit_canvas_menu, 'Back sketch', () => open_meta_editor('back_sketch'));
add_menu_item(edit_canvas_menu, 'Front sketch', () => open_meta_editor('front_sketch'));

const main_editor_menu = new Menu();
main_editor_menu.append(new MenuItem({label: 'Edit metacode', submenu: edit_canvas_menu}));

window.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    main_editor_menu.popup({ window: remote.getCurrentWindow() });
}, false);

function resize_canvases(){
    if(back_sketch){
        back_sketch.canvas.width = front_sketch.canvas.width = window.innerWidth;
        back_sketch.canvas.height = front_sketch.canvas.height = window.innerHeight;
    }
}

$(function() {
    editor = ace.edit('main_editor', {  theme: "ace/theme/monokai", 
                                        mode: "ace/mode/python",
                                        minLines: 40, 
                                        maxLines: 100, 
                                        showGutter: false,
                                        autoScrollEditorIntoView: true, 
                                        fontSize: 14 });
    editor.renderer.setPadding(10);
    editor.renderer.setScrollMargin(5, 5);
    editor.session.on('change', code_change);

    let back_canvas = $('<canvas id="back_canvas"></canvas>');
    $('.ace_marker-layer').first().after(back_canvas);
    back_canvas.css('z-index', '1');
    back_sketch = create_sketch(null, 'back_sketch', null, back_canvas.get(0));
    front_sketch = create_sketch(null, 'front_sketch', null, $('#front_canvas').get(0));
    resize_canvases();

    $('#sheet_button').click(function(){
        let win = new BrowserWindow({width:470, height: 400, x: 15, y: 30, show: true,
                            acceptFirstMouse: true, webPreferences: {nodeIntegration: true}});
        let load_path = 'C:\\hello\\there.jpg';
        win.loadURL(window.location.origin + '/sheet/sheet.html?load=' + encodeURI(load_path));
    });

    $('#save_button').click(function(){
        eel.crap();
    });

    $('#run_button').click(function(){
        eel.run_maincode(editor.getValue());
    });

    eel.get_code()(code => {
        editor.setValue(code, 1);
        $('#run_button').click();
    });
});

function code_change(delta) {
    if($('#auto_run').is(':checked')){
        $('#run_button').click();
    }
}

function update_position(x, y){
    eel.main_editor_dragged(x, y);
}





// TEMP TEMP TEMP TEMP //////
/*
var s = 0
function repeat(){
    s += 0.05;
    var x = 1.75 + Math.sin(s);
    set_editor_params(x);
    setTimeout(repeat, 15);
}

eel.expose(set_editor_params);
function set_editor_params(params){
    editor.container.style.lineHeight = params;
    editor.renderer.updateFontSize();
}

`import random

X = [random.random() for n in range(10)]

done = False
while not done:
    done = True
    for i, _ in enumerate(X):
        if i < len(X) - 1:
            a, b = X[i], X[i + 1]
            if a > b:
                done = False
                X[i], X[i + 1] = b, a
    print(X)
`

`import random

def f():
    return 123

def g():
    return 321

t = 0
for i in range(1000):
    if random.random() < 0.2:
        t += f()
    else:
        t += g()

print(t)
`*/
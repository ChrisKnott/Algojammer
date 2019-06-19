const { remote } = nodeRequire('electron');
const electron_prompt = nodeRequire('electron-prompt');
const { BrowserWindow, Menu, MenuItem, dialog } = remote;
var meta_editor_options = { width:500, height: 300, x: 100, y: 100, show: true,
                            acceptFirstMouse: true, webPreferences: {nodeIntegration: true}}

// Util functions ==================================================
function add_menu_item(menu, label, click){
    menu.append(new MenuItem({label: label, click}));
}

function prompt(title, label, on_input){
    electron_prompt({title: title, label: label}).then((answer) => {
        if(answer) {
            on_input(answer);
        }
    });
}

function open_meta_editor(guid){
    var win = new BrowserWindow(meta_editor_options);
    win.loadURL(window.location.origin + '/editor/meta_editor.html?guid=' + guid);
}

// Window level listeners ==========================================
window.addEventListener('keydown', function(e){
    eel.key_down(eel.guid(), e.key);
});

window.addEventListener('keyup', function(e){
    eel.key_up(eel.guid(), e.key);
});

window.addEventListener('mousedown', function(e){ 
    if(e.button == 0){
        eel.mouse_down(eel.guid(), e.screenX, e.screenY);
    }
});

window.addEventListener('mouseup', function(e){
    if(e.button == 0){
        eel.mouse_up(eel.guid(), e.screenX, e.screenY);
    }
});



// Constants =======================================================
var DRAW_CLEAR  = 0;
var DRAW_INK    = 1;
var DRAW_RECT   = 2;
var DRAW_LINE   = 3;
var DRAW_CIRC   = 4;
var DRAW_TEXT   = 5;




// ========================= DEBUG CRAP ==========================

var example_code = `
import random

rnd = lambda n: random.randint(0, n)
x, y = 0, 0

@jam.on_click
def func(mx, my, down):
    global x, y
    if down:
        x, y = mx, my

@jam.on_wheel
def whee(d):
    jam['test'] = d

@jam.on_refresh
def ref():
    #jam.canvas.clear()
    jam.canvas.ink(rnd(255), rnd(255), rnd(255))
    jam.canvas.circ(rnd(jam.canvas.width), rnd(100), 25 + rnd(20))

print('Hello there')
`;

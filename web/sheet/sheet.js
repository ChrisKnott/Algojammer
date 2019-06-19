var clicked_div, menu_position, fullscreen;

$(() => {
    fullscreen = {  canvas: document.getElementById('fullscreen_canvas'),
                    text:   document.getElementById('fullscreen_text')  }
    fullscreen.canvas.height = window.innerHeight;
    fullscreen.canvas.width = window.innerWidth;
    $('#fullscreen_output').hide(); // Start with fullscreen hidden

    fullscreen.text.addEventListener('DOMMouseScroll', (e) => clicked_div.sketch.on_wheel(e), false);
    fullscreen.text.addEventListener('mousewheel', (e) => clicked_div.sketch.on_wheel(e), false);
    fullscreen.text.addEventListener('wheel', (e) => clicked_div.sketch.on_wheel(e), false);
    fullscreen.text.addEventListener('mousedown', (e) => clicked_div.sketch.on_click(e), false);

    var url = new URL(window.location.href);
    var sheet = url.searchParams.get('data');
    if(sheet){
        build_sheet(JSON.parse(sheet));
    }
});

function save_sheet(){
    let sheet = {   title:      document.title,
                    left:       window.screenLeft,
                    top:        window.screenTop,
                    width:      window.outerWidth,
                    height:     window.outerHeight, 
                    sketches:   []};

    $('.sketch').each(async (i, div) => {
        console.log(div);
        sheet.sketches.push({
            label:      $(div).find('.label').html(),
            left:       $(div).css('left'),
            top:        $(div).css('top'),
            width:      $(div).find('.output').width(),
            height:     $(div).find('.output').height(),
            style:      $(div).find('.output').css('display'),
            colour:     $(div).find('.output').css('background'),
            maxed:      Boolean(div.sketch.old),
            code:       await eel.get_metacode(div.sketch.guid)(),
            animate:    div.sketch.animate
        });
    });

    dialog.showSaveDialog(  remote.getCurrentWindow(),
                            {title: 'Save sheet...', defaultPath: sheet.title + '.json'},
                            path => {
                                if(path){
                                    eel.save_to_file(sheet, path);
                                }
                            });
}

function load_sheet(){
    dialog.showOpenDialog(  remote.getCurrentWindow(), {title: 'Load sheet...'}, 
                            async paths => {
                                if(paths){
                                    let sheet = await eel.load_from_file(paths[0])();
                                    build_sheet(sheet);
                                }
                            });
}

function build_sheet(data){
    $('.sketch').each((i, s) => {
        s.sketch.animate = false;
        $(s).remove();
    });

    document.title = data.title;
    window.moveTo(data.left, data.top);
    window.resizeTo(data.width, data.height);

    $('#fullscreen_output').hide();
    $('#sketches').show();

    $.each(data.sketches, (i, s) => {
        let div = add_sketch_div(s.label, s.code, s.left, s.top, s.width, s.height);
        div.sketch.animate = s.animate;
        $(div).find('.output').css('display', s.style);
        $(div).find('.output').css('background', s.colour);
        if(s.maxed){
            clicked_div = div;
            div.sketch.fullscreen(fullscreen.text, fullscreen.canvas);
            $('#fullscreen_output').css('background', s.colour);
            $('#fullscreen_output').show();
            $('#sketches').hide();
        }
    });
}



// Build Sheet context menu ======================================================================
const sheet_menu = new Menu();
add_menu_item(sheet_menu, 'Add sketch', () => {
    prompt('Add sketch', 'Label:', (label) => {
        let code = `#Auto-generated\n`                          + 
                   `n = jam['current_step']\n`                  +
                   `try:\n`                                     +
                   `    ${label} = jam.state(n)['${label}']\n`  +
                   `    print(repr(${label}))\n`                +
                   `except KeyError:\n`                         +
                   `    print("NameError: name '${label}' is not defined")\n`;
        
        add_sketch_div(label, code, menu_position.x, menu_position.y, 100, 19);
    });
});
add_menu_item(sheet_menu, 'Auto add...', () => {});
add_menu_item(sheet_menu, 'Rename sheet', () => {
    prompt('Rename sheet', 'Title:', (title) => document.title = title);
});
add_menu_item(sheet_menu, 'Save sheet', () => save_sheet());
add_menu_item(sheet_menu, 'Load sheet', () => load_sheet());



// Sketch context menu ==============================================================================
const sketch_menu = new Menu();
add_menu_item(sketch_menu, 'Edit metacode', () => open_meta_editor(clicked_div.sketch.guid));
add_menu_item(sketch_menu, 'Set background', () => {
    prompt('Background colour', 'Background colour:', (colour) => {
        $(clicked_div).find('.output').css('background', colour);
    });
});
add_menu_item(sketch_menu, 'Maximise', () => {
    $('.sketch').each((i, div) => {
        if(div == clicked_div){
            div.sketch.fullscreen(fullscreen.text, fullscreen.canvas);
            let colour = $(clicked_div).find('.output').css('background');
            $('#fullscreen_output').css('background', colour);
            $('#fullscreen_output').show();
            $('#sketches').hide();
        } else {
            div.sketch.animate = false;
        }
    })
});
add_menu_item(sketch_menu, 'Toggle label', () => {
    let output_div = $(clicked_div).find('.output');
    let current_style = output_div.css('display');
    output_div.css('display', current_style === 'block' ? 'inline-block' : 'block');
});
add_menu_item(sketch_menu, 'Rename', () => {
    prompt('Rename sketch', 'Label:', (label) => $(clicked_div).find('.label').html(label));
});
add_menu_item(sketch_menu, 'Delete', () => clicked_div.sketch.delete());



// Fullscreen sketch context menu ==================================================================
const fullscreen_menu = new Menu();
add_menu_item(fullscreen_menu, 'Edit metacode', () => open_meta_editor(clicked_div.sketch.guid));
add_menu_item(fullscreen_menu, 'Restore', () => {
    clicked_div.sketch.restore();
    $('#fullscreen_output').hide();
    $('#sketches').show();
    $('.sketch').each((i, div) => {
        div.sketch.animate = true;
        div.sketch.draw();
    });
});
add_menu_item(fullscreen_menu, 'Save sheet', () => save_sheet());
add_menu_item(fullscreen_menu, 'Load sheet', () => load_sheet());



// Window listeners ==============================================================================
window.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    menu_position = {x: e.x, y: e.y};
    classes = e.target.classList;
    if(classes.contains('label') || classes.contains('text')){
        clicked_div = $(e.target).closest('.sketch').get(0);
        sketch_menu.popup({ window: remote.getCurrentWindow() });
    } else {
        if(e.target.id === 'fullscreen_text'){
            fullscreen_menu.popup({window: remote.getCurrentWindow()});
        } else {
            sheet_menu.popup({ window: remote.getCurrentWindow() });
        }
    }
}, false);

window.addEventListener('resize', (e) => {
    fullscreen.canvas.height = window.innerHeight;
    fullscreen.canvas.width = window.innerWidth;
});

var editor, canvas;

// FPS
//(function(){var script=document.createElement('script');script.onload=function(){var stats=new Stats();document.body.appendChild(stats.dom);requestAnimationFrame(function loop(){stats.update();requestAnimationFrame(loop)});};script.src='//rawgit.com/mrdoob/stats.js/master/build/stats.min.js';document.head.appendChild(script);})();

$(function() {
    editor = ace.edit('main_editor', {  theme: "ace/theme/monokai", 
                                        mode: "ace/mode/python",
                                        maxLines: 100, 
                                        minLines: 40, 
                                        showGutter: false,
                                        autoScrollEditorIntoView: true, 
                                        fontSize: 14  });
    editor.renderer.setPadding(10);
    editor.renderer.setScrollMargin(5, 5);
    editor.session.on('change', code_change);

    editor.setValue(code, 1);
    canvas = $('<canvas class="back-canvas"></canvas>');

    $('.ace_marker-layer').first().after(canvas);
    canvas.css('z-index', '1');

    // TEMP TEMP TEMP TEMP //////
    ctx = canvas.get(0).getContext('2d');
    window.requestAnimationFrame(clock);
    /////////////////////////////

    $('#sheet_button').click(function(){
        let geom = 'width=400, height=400, left=100, top=100';
        window.open('/sheet/sheet.html?' + Math.random(), '_blank', geom);
    });

    $('#save_button').click(function(){
        eel.crap();
    });

    $('#run_button').click(function(){
        eel.run(editor.getValue());
    });

    update_position(window.screenX, window.screenY);

    console.log(editor.container.style.lineHeight);
    //repeat();
});

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

function code_change(delta) {
    if($('#auto_run').is(':checked')){
        $('#run_button').click();
    }
}

function update_position(x, y){
    eel.main_editor_dragged(x, y);
}

// TEMP TEMP TEMP TEMP //////
var code = `import random

X = [random.random() for n in range(100)]

done = False
while not done:
    done = True
    for i, _ in enumerate(X):
        if i < len(X) - 1:
            a, b = X[i], X[i + 1]
            if a > b:
                done = False
                X[i], X[i + 1] = b, a
`;

code = `import random

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
`;


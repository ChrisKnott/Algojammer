var editor;
var lines = [];
var visits = [];
var hash;
var shift_key = false;

// FPS
//(function(){var script=document.createElement('script');script.onload=function(){var stats=new Stats();document.body.appendChild(stats.dom);requestAnimationFrame(function loop(){stats.update();requestAnimationFrame(loop)});};script.src='//rawgit.com/mrdoob/stats.js/master/build/stats.min.js';document.head.appendChild(script);})();

$(function() {
    editor = ace.edit('editor', {theme: "ace/theme/monokai", mode: "ace/mode/python",
                                 maxLines: 100, minLines: 40, showGutter: false,
                                 autoScrollEditorIntoView: true, fontSize: 14 });
    editor.renderer.setPadding(10);
    editor.renderer.setScrollMargin(5, 5);
    editor.session.on('change', code_change);
    editor.highlight = editor.session.addMarker(new ace.Range(0, 0, 0, 1), 
                                                'line_highlight', 'fullLine');

    $('#run_button').click(function(){
        lines = [], visits = [];
        hash = md5(editor.getValue());
        eel.run(editor.getValue());
    });

    $('#state_button').click(function(){
        var geom = 'width=500, height=800, left=100, top=200, resizeable=no';
        window.open('state.html', '_blank', geom);
    });

    $('#io_button').click(function(){
        // TODO: need to be able to read from stdin (overwrite __stdin__ with StringIO)
        // stdout console should show state of stdout at Current Step
        // This is necessary for GCJ problems
    });

    $('#save_button').click(function(){
        eel.save_file(editor.getValue());
    })

    $('#load_button').click(function(){
        eel.load_file()
    });

    $(window).keyup(window_keyup);
    $(window).keydown(window_keydown);

    init_timeline();
    eel.read_example(); // TODO: temp
});

function code_change(delta) {
    lines = [];     // Clear previous execution
    visits = [];
    if($('#auto_run').is(':checked')){
        $('#run_button').click();
    }
}

eel.expose(execution_report);
function execution_report(data) {
    if(data.hash === hash){
        var shift = lines.length;
        lines = lines.concat(data.line);
        $.each(data.line, function(i, l){
            if(l > visits.length){
                for(var j = visits.length; j < l; j++){
                    visits.push([]);
                }
            }
            visits[l - 1].push(i + shift);
        });
        zoom_timeline(0);
    }
}

eel.expose(set_code);
function set_code(code){
    editor.setValue(code, 1);
}

function highlight_line(n){
    var row = editor.session.getMarkers()[editor.highlight];
    row.range.start.row = row.range.end.row = n - 1;
    editor.updateSelectionMarkers();
}

Array.prototype.bisect = function(searchElement) {
    var minIndex = 0, maxIndex = this.length - 1;
    var currentIndex, currentElement;
    while (minIndex < maxIndex) {
        currentIndex = Math.floor((minIndex + maxIndex) / 2);
        currentElement = this[currentIndex];
        if (currentElement < searchElement) {
            minIndex = currentIndex + 1;
        } else {
            maxIndex = currentIndex - 1;
        }
    }
    return minIndex;
}

function window_keydown(evt){
    if(evt.key == 'Shift'){
        shift_key = true;
    }
}

function window_keyup(evt){
    if(evt.key == 'Shift'){
        shift_key = false;
    }
}

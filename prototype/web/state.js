var clicked_box = null;

$(function() {
    init_box_menu();
    $('#menu').menu({select: menu_select});

    $(document).contextmenu(function(e){
        var options = {my: 'left top', of: e, collision: 'fit'};
        if(e.target.tagName === 'HTML'){
            e.preventDefault();
            $('#menu').show().position(options);
        } else if(e.target.classList.contains('label')){
            e.preventDefault();
            clicked_box = $(e.target).parent();
            $('#box_menu').show().position(options);
        }
    });

    $(document).click(function(e){
        $('#menu').hide();
        $('#box_menu').hide();
    });
    $(document).click();    // Hide context menus
});

function menu_select(e, ui) {
    var choice = $(e.currentTarget).text();
    if(choice === 'Add'){
        add_expr(prompt('Add...'), e.clientX - 8, e.clientY - 8);
    } else if(choice === 'Add all') {
        add_all_expr();
    } else if(choice === 'Save') {
        var boxes = [];
        $('.state_box').each(function(i, box){
            var data = {id:     $(box).attr('id'), 
                        expr:   $(box).attr('expr'),
                        left:   $(box).css('left'),
                        top:    $(box).css('top')}

            // If box has been resized, add width/height
            if($(box).find('.value')[0].style.width){
                data.width = $(box).find('.value').width();
                data.height = $(box).find('.value').height();
            }

            boxes.push(data);
        });
        eel.save_state_boxes(boxes);
    } else if(choice === 'Load') {
        eel.load_state_boxes()(add_boxes);
    }
}

function box_menu_select(e, ui) {
    var uid = clicked_box.attr('id');
    var choice = $(e.currentTarget);
    if(choice.attr('is_template')){
        var expr = clicked_box.attr('expr')
        var code = choice.attr('code').replace('%expr', expr)
        eel.set_state_box_code(uid, code)
    } else {
        if(choice.text() === 'Delete'){
            clicked_box.remove();
            eel.delete_state_box(uid);
        } else if(choice.text() === 'Edit'){
            var url = 'state_editor.html?uid=' + uid
            window.open(url, '_blank', 'width=500, height=500');
        }
    }
}

function add_boxes(box_info) {
    $.each(box_info, function(i, box){
        add_state_box(box['expr'], box['code'], box['left'], 
                      box['top'], box['width'], box['height']);
    });
}

function add_expr(expr, x, y){
    if(expr != null && expr.length > 0){
        var code = 'print(repr(' + expr + '))'
        add_state_box(expr, code, x, y);
    }
}

async function add_all_expr() {
    var exprs = await eel.get_all_variables()();
    $.each(exprs, function(i, expr){
        add_expr(expr, 5, 5 + i * 25);
    });
}

function add_state_box(expr, code, x, y, width, height){
    var uid = ('box' + Date.now() + Math.random()).replace('.', '');
    var state_box = $('<div class="state_box"> \
                           <div class="label" /><div class="value" /> \
                       </div>');

    state_box.find('.label').html(expr);
    state_box.find('.value').html('&#8203;')
                            .width(width).height(height);
    state_box.css('left', x).css('top', y);
    state_box.attr('id', uid);
    state_box.attr('expr', expr)

    $('body').append(state_box);

    state_box.draggable({ handle: ".label" });
    state_box.find('.value').resizable({ handles: "se", autoHide: true });

    eel.set_state_box_code(uid, code);
}

eel.expose(set_state_box_value);
function set_state_box_value(uid, value) {
    if(value === ''){
        value = '&#8203;'   // Use zero width space instead of nothing (to keep DOM node)
    }
    $('#' + uid).find('.value').contents().first().replaceWith(value);
}

async function init_box_menu(){
    var templates = await eel.get_state_box_templates()();
    add_templates($('#template_menu'), templates['templates']);
    $('#box_menu').menu({select: box_menu_select});
}

function add_templates(li, folder){
    var ul = $('<ul>')
    $.each(folder, function(name, contents){
        var li = $('<li><div>' + name + '</div></li>');
        if(typeof contents === 'string'){
            li.attr({'is_template': true, 
                     'code': contents});
        } else {
            add_templates(li, contents);
        }
        ul.append(li);
    });
    li.append(ul);
}

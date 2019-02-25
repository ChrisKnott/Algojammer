const { remote } = nodeRequire('electron');
const { Menu, MenuItem } = remote;

const menu = new Menu();
menu.append(new MenuItem({ label: 'Dev Tools', click() { 
	remote.getCurrentWindow().toggleDevTools(); 
}}));

window.addEventListener('contextmenu', (e) => {
  e.preventDefault()
  menu.popup({ window: remote.getCurrentWindow() })
}, false);

eel.expose(set_window_position);
function set_window_position(guid, x, y){
	if(guid == eel.guid()){
    	window.moveTo(x, y);
	}
}

window.addEventListener('keydown', function(e){
	eel.key_down(eel.guid(), e.key);
});

window.addEventListener('keyup', function(e){
	eel.key_up(eel.guid(), e.key);
});

window.addEventListener('mousedown', function(e){ 
	if(e.button == 0){
		eel.mouse_down(eel.guid(), e.clientX, e.clientY);
	}
});

window.addEventListener('mouseup', function(e){
	if(e.button == 0){
		eel.mouse_up(eel.guid(), e.clientX, e.clientY);
	}
});

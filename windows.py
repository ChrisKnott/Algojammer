import eel

main_editor = {}
sheets = {}

@eel.expose
def main_editor_dragged(x, y):
	main_editor['x'], main_editor['y'] = x, y
	for guid, (cx, cy, dx, dy) in list(sheets.items()):
		if (dx, dy) == (None, None):
			dx, dy = cx - x, cy - y
			sheets[guid] = (cx, cy, dx, dy)

@eel.expose
def sheet_dragged(guid, x, y):
	cx, cy, dx, dy = x, y, None, None	
	if main_editor:
		dx = x - main_editor['x']
		dy = y - main_editor['y']
	sheets[guid] = (cx, cy, dx, dy)

# Background thread to move Sheets smoothly (mainly for Mac)
def move_sheets_smoothly():
	while True:
		eel.sleep(0.01)
		if main_editor:
			for guid, (cx, cy, dx, dy) in list(sheets.items()):
				tx, ty = main_editor['x'] + dx, main_editor['y'] + dy
				diff = abs(cx - tx) + abs(cy - ty)
				if diff > 0:
					if abs(cx - tx) + abs(cy - ty) > 0.5:
						# Move window half way to target
						cx += (tx - cx) / 2
						cy += (ty - cy) / 2
					else:
						cx, cy = tx, ty
					
					sheets[guid] = (cx, cy, dx, dy)
					eel.set_window_position(guid, cx, cy)

eel.spawn(move_sheets_smoothly)

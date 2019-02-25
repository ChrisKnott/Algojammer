# Class that saves up drawing history so that it can be recreated in JS

class Canvas:
	def __init__(self, w, h):
		self._commands = []	# Recorded list of draw calls
		self._last_ink = None
		self.width = w
		self.height = h
		self.mx = 0			# Mouse x
		self.my = 0			# Mouse y

		# Drawing commands
		self.clear = lambda:            self._add_command(0)
		self.ink   = lambda r, g, b:    self._add_command(1, r, g, b)
		self.rect  = lambda x, y, w, h: self._add_command(2, x, y, w, h)
		self.line  = lambda x, y, a, b: self._add_command(3, x, y, a, b)
		self.circ  = lambda x, y, r:    self._add_command(4, x, y, r)
		self.text  = lambda x, y, s, p:	self._add_command(5, x, y, s, p)

	def _add_command(self, c, *args):
		# Optimisations to ignore clear() and ink() calls with no effect
		if c == 0:
			if self._commands and self._commands[-1][0] == 0:
				return
		elif c == 1:
			if args == self._last_ink:
				return
			else:
				self._last_ink = args
		
		self._commands += [(c, args)]

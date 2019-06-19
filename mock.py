import io, sys, gevent

class MockIO:
	def __init__(self, stdin_str=None):
		self.stdout = io.StringIO()
		self.stdin = io.StringIO(stdin_str)
		self.stderr = self.stdout #io.StringIO()
		self._i = 0
		self.input_callback = None
		self.print_callback = None

	def get_print_function(self):
		def print_function(*args, **kwargs):
			sys.stdout, stdout = self.stdout, sys.stdout
			sys.stderr, stderr = self.stderr, sys.stderr
			print(*args, **kwargs)
			sys.stdout = stdout
			sys.stderr = stdout	#stderr
			if self.print_callback:
				self.print_callback()

		return print_function

	def get_input_function(self):
		def input_function(*args, **kwargs):
			while True:
				try:
					sys.stdin, stdin = self.stdin, sys.stdin
					read = input(*args, **kwargs)
					break
				except EOFError:
					sys.stdin = stdin
					gevent.sleep(0.001)
			sys.stdin = stdin
			if self.input_callback:
				self.input_callback(read)

			return read
		return input_function

	def functions(self):
		return {'print': self.get_print_function(),
				'input': self.get_input_function()}

	def feed_input(self, s):
		n = self.stdin.tell()
		self.stdin.read()
		self.stdin.write(s)
		self.stdin.seek(n)

	def get_output(self):
		return self.stdout.getvalue()

	def get_new_output(self):
		output = self.get_output()
		new_output = output[self._i:]
		self._i = len(output)
		return new_output

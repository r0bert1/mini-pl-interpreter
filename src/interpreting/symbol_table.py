class SymbolTable:
	def __init__(self):
		self.symbols = {}

	def get(self, name):
		return self.symbols.get(name, None)

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]
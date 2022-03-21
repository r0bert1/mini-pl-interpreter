from error import RunTimeError
from interpreting.context import Context
from interpreting.symbol_table import SymbolTable
from interpreting.result import RunTimeResult

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def illegal_operation(self, other=None):
		if not other: other = self
		return RunTimeError(
			self.pos_start, other.pos_end,
			'Illegal operation'
		)
	
	def __repr__(self):
		return f'"{self.value}"'

class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def plus(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None

	def minus(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None

	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None

	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RunTimeError(
					other.pos_start, other.pos_end,
					"Division by zero"
				)

			return Number(self.value / other.value).set_context(self.context), None

	def equals(self, other):
		if isinstance(other, Number):
			return Number(int(self.value == other.value)).set_context(self.context), None

	def less_than(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None

	def not_(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def and_(self, other):
		if isinstance(other, Number):
			return Number(int(self.value and other.value)).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def plus(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements
  
	def copy(self):
		copy = List(self.elements)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return ", ".join([str(x) for x in self.elements])

	def __repr__(self):
		return f'[{", ".join([repr(x) for x in self.elements])}]'
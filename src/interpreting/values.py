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

"""class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RunTimeResult()

		if len(args) > len(arg_names):
			return res.failure(RunTimeError(
			self.pos_start, self.pos_end,
			f"{len(args) - len(arg_names)} too many args passed into {self}",
			self.context
			))

		if len(args) < len(arg_names):
			return res.failure(RunTimeError(
			self.pos_start, self.pos_end,
			f"{len(arg_names) - len(args)} too few args passed into {self}",
			self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RunTimeResult()
		res.register(self.check_args(arg_names, args))
		if res.error: return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RunTimeResult()
		exec_ctx = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.error: return res

		return_value = res.register(method(exec_ctx))
		if res.error: return res
		return res.success(return_value)
  
	def no_visit_method(self, node, context):
		raise Exception(f'No execute_{self.name} method defined')

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<built-in function {self.name}>"

	def execute_print(self, exec_ctx):
		print(str(exec_ctx.symbol_table.get('value')))
		return RunTimeResult().success(Number.null)
	execute_print.arg_names = ['value']

	def execute_input(self, exec_ctx):
		text = input()
		return RunTimeResult().success(String(text))
	execute_input.arg_names = []

	def execute_is_number(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
		return RunTimeResult().success(Number.true if is_number else Number.false)
	execute_is_number.arg_names = ["value"]

BuiltInFunction.print       = BuiltInFunction("print")
BuiltInFunction.input       = BuiltInFunction("input")
BuiltInFunction.is_number   = BuiltInFunction("is_number")"""
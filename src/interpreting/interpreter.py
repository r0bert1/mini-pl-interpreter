from nodes import *
from interpreting.values import Number, String, List
from tokens import TokenType
from interpreting.result import RunTimeResult
from error import RunTimeError

class Interpreter:
	def evaluate(self, node, context):
		method_name = f'evaluate_{type(node).__name__}'
		method = getattr(self, method_name)
		return method(node, context)

	def no_evaluate_method(self, node):
		raise Exception(f"No evaluate_{type(node).__name__} method defined")
		
	def evaluate_NumberNode(self, node, context):
		return RunTimeResult().success(
			Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def evaluate_StringNode(self, node, context):
		return RunTimeResult().success(
			String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def evaluate_BinaryOpNode(self, node, context):
		result = RunTimeResult()
		left_side = result.register(self.evaluate(node.left_node, context))
		if result.error: return result
		right_side = result.register(self.evaluate(node.right_node, context))
		if result.error: return result

		if node.op_token.type == TokenType.PLUS:
			value, error = left_side.plus(right_side)

		if node.op_token.type == TokenType.MINUS:
			value, error = left_side.minus(right_side)

		if node.op_token.type == TokenType.MULTIPLY:
			value, error = left_side.multiplied_by(right_side)

		if node.op_token.type == TokenType.DIVIDE:
			value, error = left_side.divided_by(right_side)

		if node.op_token.type == TokenType.EQUALS:
			value, error = left_side.equals(right_side)

		if node.op_token.type == TokenType.LT:
			value, error = left_side.less_than(right_side)

		if node.op_token.type == TokenType.AND:
			value, error = left_side.and_(right_side)

		if error: return result.failure(error)

		return result.success(value.set_pos(node.pos_start, node.pos_end))

	def evaluate_UnaryOpNode(self, node, context):
		result = RunTimeResult()
		value = result.register(self.evaluate(node.node, context))
		if result.error: return result

		if node.op_token.type == TokenType.MINUS:
			value, error = value.multiplied_by(Number(-1))

		if node.op_token.type == TokenType.NOT:
			value, error = value.not_()
		
		if error: return result.failure(error)
		
		return result.success(value.set_pos(node.pos_start, node.pos_end))

	def evaluate_VarAccessNode(self, node, context):
		result = RunTimeResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)['value']

		if not value:
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is not defined"
			))

		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return result.success(value)

	def evaluate_VarAssignNode(self, node, context):
		result = RunTimeResult()
		var_name = node.var_name_token.value
		value = result.register(self.evaluate(node.value_node, context))
		
		if node.var_type_token:
			var_type = node.var_type_token.value
		else:
			if not context.symbol_table.get(var_name):
				return result.failure(RunTimeError(
					node.pos_start, node.pos_end,
					f"'{var_name}' is not defined"
				))
			var_type = context.symbol_table.get(var_name)['type']

		if var_type == 'int' and not isinstance(value, Number):
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"Expected an integer to be assigned to '{var_name}'"
			))
		if var_type == 'string' and not isinstance(value, String):
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"Expected a string to be assigned to '{var_name}'"
			))
		if result.error: return result

		context.symbol_table.set(var_name, {'value': value, 'type': var_type})
		return result.success(value)

	def evaluate_VarDeclarationNode(self, node, context):
		result = RunTimeResult()
		var_name = node.var_name_token.value
		var = context.symbol_table.get(var_name)
		if var:
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is already declared"
			))
		
		var_type = node.var_type_token.value
		context.symbol_table.set(var_name, {'value': None, 'type': var_type})
		return result.success(None)

	def evaluate_ForNode(self, node, context):
		result = RunTimeResult()
		elements = []

		var = context.symbol_table.get(node.var_name_token.value)

		if not var:
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"'{node.var_name_token.value}' is not defined"
			))

		if var['type'] != 'int':
			return result.failure(RunTimeError(
				node.pos_start, node.pos_end,
				f"Expected loop variable '{node.var_name_token.value}' to be an integer"
			))

		start_value = result.register(self.evaluate(node.start_value_node, context))
		if result.error: return result

		end_value = result.register(self.evaluate(node.end_value_node, context))
		if result.error: return result

		i = start_value.value
		
		while i < int(end_value.value):
			context.symbol_table.set(node.var_name_token.value, {'value': Number(i), 'type': 'int'})
			i += 1

			elements.append(result.register(self.evaluate(node.body_node, context)))
			if result.error: return result

		return result.success(
			Number.null if node.should_return_null else
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def evaluate_CallNode(self, node, context):
		result = RunTimeResult()

		if node.func_token.value == 'print':
			if node.arg_token.type == TokenType.STRING:
				print(node.arg_token.value)
				return RunTimeResult().success(Number.null)
			
			if node.arg_token.type == TokenType.IDENTIFIER:
				var_name = node.arg_token.value
				value = context.symbol_table.get(var_name)['value']

				if not value:
					return result.failure(RunTimeError(
						node.pos_start, node.pos_end,
						f"'{var_name}' is not defined"
					))

				print(value)
				return RunTimeResult().success(Number.null)

		if node.func_token.value == 'read':
			var_name = node.arg_token.value
			var_type = context.symbol_table.get(var_name)['type']

			if not var_type:
				return result.failure(RunTimeError(
					node.pos_start, node.pos_end,
					f"'{var_name}' has not been declared"
				))
			
			text = input()
			
			if var_type == 'int':
				try:
					text = int(text)
				except Exception:
					return result.failure(RunTimeError(
						node.pos_start, node.pos_end,
						f"Expected an integer to be assigned to '{var_name}'"
					))
				context.symbol_table.set(node.arg_token.value, {'value': Number(text), 'type': var_type})
				return result.success(Number(text))
			else:
				context.symbol_table.set(node.arg_token.value, {'value': String(text), 'type': var_type})
				return result.success(String(text))

		return result.success(None)

	def evaluate_ListNode(self, node, context):
		res = RunTimeResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.evaluate(element_node, context)))
			if res.error: return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

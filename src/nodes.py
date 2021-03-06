class VarAccessNode:
	def __init__(self, var_name_token):
		self.var_name_token = var_name_token

		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.var_name_token.pos_end

class VarAssignNode:
	def __init__(self, var_name_token, value_node, var_type_token=None):
		self.var_name_token = var_name_token
		self.var_type_token = var_type_token
		self.value_node = value_node

		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.value_node.pos_end

class VarDeclarationNode:
	def __init__(self, var_name_token, var_type_token):
		self.var_name_token = var_name_token
		self.var_type_token = var_type_token

		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.var_type_token.pos_end

class NumberNode:
	def __init__(self, token):
		self.token = token
		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end

	def __repr__(self):
		return f"{self.token}"

class StringNode:
	def __init__(self, token):
		self.token = token
		self.pos_start = self.token.pos_start
		self.pos_end = self.token.pos_end

	def __repr__(self):
		return f"{self.token}"

class BinaryOpNode:
	def __init__(self, left_node, op_token, right_node):
		self.left_node = left_node
		self.op_token = op_token
		self.right_node = right_node
		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f"({self.left_node}, {self.op_token}, {self.right_node})"

class UnaryOpNode:
	def __init__(self, op_token, node):
		self.op_token = op_token
		self.node = node
		self.pos_start = self.op_token.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return f"({self.op_token}, {self.node})"

class ForNode:
	def __init__(self, var_name_token, start_value_node, end_value_node, body_node, should_return_null):
		self.var_name_token = var_name_token
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.pos_start = self.var_name_token.pos_start
		self.pos_end = self.body_node.pos_end

class CallNode:
	def __init__(self, func_token, arg_token):
		self.func_token = func_token
		self.arg_token = arg_token

		self.pos_start = self.func_token.pos_start
		self.pos_end = self.arg_token.pos_end

class ListNode:
	def __init__(self, element_nodes, pos_start, pos_end):
		self.element_nodes = element_nodes

		self.pos_start = pos_start
		self.pos_end = pos_end
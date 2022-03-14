from dataclasses import dataclass

@dataclass
class NumberNode:
	value: any

	def __repr__(self):
		return f"{self.value}"

@dataclass
class BinaryOpNode:
	left_node: any
	op_token: any
	right_node: any

	def __repr__(self):
		return f"({self.left_node}, {self.op_token}, {self.right_node})"
	
@dataclass
class MinusNode:
	node: any

	def __repr__(self):
		return f"(-{self.node})"
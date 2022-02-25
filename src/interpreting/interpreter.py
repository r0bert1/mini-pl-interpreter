from nodes import *
from interpreting.values import Number

class Interpreter:
	def evaluate(self, node):
		method_name = f'evaluate_{type(node).__name__}'
		method = getattr(self, method_name)
		return method(node)
		
	def evaluate_NumberNode(self, node):
		return Number(node.value)

	def evaluate_AddNode(self, node):
		return Number(self.evaluate(node.node_a).value + self.evaluate(node.node_b).value)

	def evaluate_SubtractNode(self, node):
		return Number(self.evaluate(node.node_a).value - self.evaluate(node.node_b).value)

	def evaluate_MultiplyNode(self, node):
		return Number(self.evaluate(node.node_a).value * self.evaluate(node.node_b).value)

	def evaluate_DivideNode(self, node):
		try:
			return Number(self.evaluate(node.node_a).value / self.evaluate(node.node_b).value)
		except:
			raise Exception("Runtime math error")

	def evaluate_PlusNode(self, node):
		return self.evaluate(node.node)

	def evaluate_MinusNode(self, node):
		return Number(-self.evaluate(node.node).value)

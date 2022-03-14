from tokens import TokenType
from nodes import *
from error import InvalidSyntaxError

class Parser:
	def __init__(self, tokens):
		self.tokens = iter(tokens)
		self.token_index = -1
		self.get_next_token()

	def raise_error(self):
		raise InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, f"{self.current_token}")
	
	def get_next_token(self):
		self.token_index += 1
		try:
			self.current_token = next(self.tokens)
		except StopIteration:
			self.current_token = None

	def parse(self):
		return self.expression()

	def expression(self):
		return self.binary_op(self.term, (TokenType.PLUS, TokenType.MINUS))

	def term(self):
		return self.binary_op(self.factor, (TokenType.MULTIPLY, TokenType.DIVIDE))

	def binary_op(self, function, op_tokens):
		op_left_side = function()

		while self.current_token != None and self.current_token.type in op_tokens:
			op_token = self.current_token
			self.get_next_token()
			op_right_side = function()
			op_left_side = BinaryOpNode(op_left_side, op_token, op_right_side)
				
		return op_left_side

	def factor(self):
		token = self.current_token

		if token.type == TokenType.LPAREN:
			self.get_next_token()
			result = self.expression()

			if self.current_token.type != TokenType.RPAREN:
				self.raise_error()
			
			self.get_next_token()
			return result

		elif token.type in (TokenType.INTEGER, TokenType.FLOAT):
			self.get_next_token()
			return NumberNode(token.value)
		
		elif token.type == TokenType.MINUS:
			self.get_next_token()
			return MinusNode(self.factor())
		
		self.raise_error()
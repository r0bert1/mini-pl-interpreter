from tokens import TokenType
from nodes import *
from error import InvalidSyntaxError
from parsing.result import ParseResult

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
		result = self.expression()
		if not result.error and self.current_token.type != TokenType.EOF:
			return result.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected '+', '-', '*' or '/'"
			))
		
		return result

	def expression(self):
		result = ParseResult()

		if self.current_token.matches(TokenType.KEYWORD, 'VAR'):
			result.register_advancement()
			self.get_next_token()

			if self.current_token.type != TokenType.IDENTIFIER:
				return result.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected identifier"
				))

			var_name = self.current_token
			result.register_advancement()
			self.get_next_token()

			if self.current_token.type != TokenType.EQUALS:
				return result.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected '='"
				))

			result.register_advancement()
			self.get_next_token()
			expression = result.register(self.expression())
			if result.error: return result
			return result.success(VarAssignNode(var_name, expression))


		node = result.register(self.binary_op(self.term, (TokenType.PLUS, TokenType.MINUS)))

		if result.error:
			return result.failure(InvalidSyntaxError(
				self.current_token.pos_start, self.current_token.pos_end,
				"Expected 'VAR', int, float, identifier, '+', '-' or '('"
			))

		return result.success(node)


	def term(self):
		return self.binary_op(self.factor, (TokenType.MULTIPLY, TokenType.DIVIDE))

	def binary_op(self, function, op_tokens):
		result = ParseResult()
		op_left_side = result.register(function())
		if result.error: return result

		while self.current_token != None and self.current_token.type in op_tokens:
			op_token = self.current_token
			result.register_advancement()
			self.get_next_token()
			op_right_side = result.register(function())
			if result.error: return result
			op_left_side = BinaryOpNode(op_left_side, op_token, op_right_side)
				
		return result.success(op_left_side)

	def factor(self):
		result = ParseResult()
		token = self.current_token

		if token.type == TokenType.LPAREN:
			result.register_advancement()
			self.get_next_token()
			expression = result.register(self.expression())
			if result.error: return result

			if self.current_token.type != TokenType.RPAREN:
				return result.failure(InvalidSyntaxError(
					self.current_token.pos_start, self.current_token.pos_end,
					"Expected ')'"
				))

			result.register_advancement()
			self.get_next_token()
			return result.success(expression)
		
		elif token.type == TokenType.IDENTIFIER:
			result.register_advancement()
			self.get_next_token()
			return result.success(VarAccessNode(token))

		elif token.type in (TokenType.MINUS, TokenType.PLUS):
			result.register_advancement()
			self.get_next_token()
			factor = result.register(self.factor())
			if result.error: return result
			return result.success(UnaryOpNode(token, factor))

		elif token.type in (TokenType.INTEGER, TokenType.FLOAT):
			result.register_advancement()
			self.get_next_token()
			return result.success(NumberNode(token))
		
		return result.failure(InvalidSyntaxError(
			token.pos_start, token.pos_end,
			"Expected int, float, identifier, '+', '-' or '('"
		))
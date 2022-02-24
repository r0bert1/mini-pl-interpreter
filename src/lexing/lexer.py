from tokens import Token, TokenType

class Lexer:
	def __init__(self, text):
		self.text = iter(text)
		self.get_next_char()

	def get_next_char(self):
		try:
			self.current_char = next(self.text)
		except StopIteration:
			self.current_char = None

	def generate_tokens(self):
		while self.current_char != None:
			match self.current_char:
				case ' '|'\n'|'\t':
					self.get_next_char()
				case '.'|'0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
					yield self.generate_number()
				case '+':
					self.get_next_char()
					yield Token(TokenType.PLUS)
				case '-':
					self.get_next_char()
					yield Token(TokenType.MINUS)
				case '*':
					self.get_next_char()
					yield Token(TokenType.MULTIPLY)
				case '/':
					self.get_next_char()
					yield Token(TokenType.DIVIDE)
				case '(':
					self.get_next_char()
					yield Token(TokenType.LPAREN)
				case ')':
					self.get_next_char()
					yield Token(TokenType.RPAREN)
				case _:
					raise Exception(f"Unrecognized character: '{self.current_char}'")

	def generate_number(self):
		decimal_point_count = 0
		number_str = self.current_char
		self.get_next_char()

		while self.current_char != None and (self.current_char == '.' or self.current_char in '0123456789'):
			if self.current_char == '.':
				decimal_point_count += 1
				if decimal_point_count > 1:
					raise Exception(f"Invalid token: '{number_str}'")
			
			number_str += self.current_char
			self.get_next_char()

		if number_str.startswith('.'):
			number_str = '0' + number_str
		if number_str.endswith('.'):
			number_str += '0'

		return Token(TokenType.NUMBER, float(number_str))
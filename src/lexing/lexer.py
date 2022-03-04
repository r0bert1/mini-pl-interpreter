from tokens import Token, TokenType
from position import Position
from error import IllegalCharError
import string

WHITESPACE = ' \n\t'
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_AND_DIGITS = LETTERS + DIGITS
KEYWORDS = ['VAR']

class Lexer:
	def __init__(self, file_name, text):
		self.text = iter(text)
		self.pos = Position(-1, 0, -1, file_name, text)
		self.current_char = None
		self.get_next_char()

	def get_next_char(self):
		try:
			self.pos.advance(self.current_char)
			self.current_char = next(self.text)
		except StopIteration:
			self.current_char = None

	def generate_tokens(self):
		while self.current_char != None:
			try:
				if self.current_char in WHITESPACE:
					self.get_next_char()
				elif self.current_char == '.' or self.current_char in DIGITS:
					yield self.generate_number()
				elif self.current_char in LETTERS:
					yield self.generate_identifier()
				elif self.current_char == '+':
					self.get_next_char()
					yield Token(TokenType.PLUS, pos_start=self.pos)
				elif self.current_char == '-':
					self.get_next_char()
					yield Token(TokenType.MINUS, pos_start=self.pos)
				elif self.current_char == '*':
					self.get_next_char()
					yield Token(TokenType.MULTIPLY, pos_start=self.pos)
				elif self.current_char == '/':
					self.get_next_char()
					yield Token(TokenType.DIVIDE, pos_start=self.pos)
				elif self.current_char == '(':
					self.get_next_char()
					yield Token(TokenType.LPAREN, pos_start=self.pos)
				elif self.current_char == ')':
					self.get_next_char()
					yield Token(TokenType.RPAREN, pos_start=self.pos)
				elif self.current_char == '=':
					self.get_next_char()
					yield Token(TokenType.EQUALS, pos_start=self.pos)
				else:
					pos_start = self.pos.copy()
					char = self.current_char
					self.get_next_char()
					raise IllegalCharError(pos_start, self.pos, f"'{char}'")
			except Exception as e:
				print(e)

	def generate_number(self):
		decimal_point_count = 0
		number_str = self.current_char
		pos_start = self.pos.copy()
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

		return Token(TokenType.NUMBER, float(number_str), pos_start, self.pos)

	def generate_identifier(self):
		id = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_AND_DIGITS + '_':
			id += self.current_char
			self.get_next_char()

		token_type = TokenType.KEYWORD if id in KEYWORDS else TokenType.IDENTIFIER

		return Token(token_type, id, pos_start, self.pos)
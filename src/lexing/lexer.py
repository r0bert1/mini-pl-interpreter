from tokens import Token, TokenType
from position import Position
from error import IllegalCharError, ExpectedCharError
import string

WHITESPACE = ' \n\t'
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_AND_DIGITS = LETTERS + DIGITS
KEYWORDS = ['var', 'for', 'in', 'do', 'end', 'print', 'read', 'end', 'int', 'string']

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
		tokens = []

		while self.current_char != None:
				if self.current_char in WHITESPACE:
					self.get_next_char()
				elif self.current_char == ';':
					tokens.append(Token(TokenType.NEWLINE, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char in DIGITS:
					tokens.append(self.generate_integer())
				elif self.current_char in LETTERS:
					tokens.append(self.generate_identifier())
				elif self.current_char == '"':
					tokens.append(self.generate_string())
				elif self.current_char == '+':
					tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '-':
					tokens.append(Token(TokenType.MINUS, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '*':
					tokens.append(Token(TokenType.MULTIPLY, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '/':
					tokens.append(Token(TokenType.DIVIDE, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '(':
					tokens.append(Token(TokenType.LPAREN, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == ')':
					tokens.append(Token(TokenType.RPAREN, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '=':
					tokens.append(Token(TokenType.EQUALS, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == ':':
					tokens.append(self.generate_assignment())
				elif self.current_char == '!':
					tokens.append(Token(TokenType.NOT, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '<':
					tokens.append(Token(TokenType.LT, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '&':
					tokens.append(Token(TokenType.AND, pos_start=self.pos))
					self.get_next_char()
				elif self.current_char == '.':
					tokens.append(self.generate_range())
				else:
					pos_start = self.pos.copy()
					char = self.current_char
					self.get_next_char()
					return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
		
		tokens.append(Token(TokenType.EOF, pos_start=self.pos))
		return tokens, None

	def generate_integer(self):
		number_str = self.current_char
		pos_start = self.pos.copy()
		self.get_next_char()

		while self.current_char != None and self.current_char in DIGITS:
			number_str += self.current_char
			self.get_next_char()
			
		return Token(TokenType.INTEGER, int(number_str), pos_start, self.pos)

	def generate_identifier(self):
		id = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_AND_DIGITS + '_':
			id += self.current_char
			self.get_next_char()

		token_type = TokenType.KEYWORD if id in KEYWORDS else TokenType.IDENTIFIER

		return Token(token_type, id, pos_start, self.pos)

	def generate_assignment(self):
		pos_start = self.pos.copy()
		self.get_next_char()

		if self.current_char == '=':
			self.get_next_char()
			return Token(TokenType.ASSIGN, pos_start=pos_start, pos_end=self.pos)

		self.get_next_char()
		return Token(TokenType.TYPEDEF, pos_start=pos_start, pos_end=self.pos)

	def generate_range(self):
		pos_start = self.pos.copy()
		self.get_next_char()

		if self.current_char == '.':
			self.get_next_char()
			return Token(TokenType.RANGE, pos_start=pos_start, pos_end=self.pos)

		self.get_next_char()
		return None, ExpectedCharError(pos_start, self.pos, "'.' (after '.')")

	def generate_string(self):
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.get_next_char()

		escape_characters = {
			'n': '\n',
			't': '\t'
		}

		while self.current_char != None and (self.current_char != '"' or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
			else:
				if self.current_char == '\\':
					escape_character = True
				else:
					string += self.current_char
			self.get_next_char()
			escape_character = False
		
		self.get_next_char()
		return Token(TokenType.STRING, string, pos_start, self.pos)
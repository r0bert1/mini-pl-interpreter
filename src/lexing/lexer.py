class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return self.type + (f":{self.value}" if self.value != None else "")

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
				case '+':
					self.get_next_char()
					yield Token('PLUS')
				case '-':
					self.get_next_char()
					yield Token('MINUS')
				case '*':
					self.get_next_char()
					yield Token('MULTIPLY')
				case '/':
					self.get_next_char()
					yield Token('DIVIDE')
				case '(':
					self.get_next_char()
					yield Token('LPAREN')
				case ')':
					self.get_next_char()
					yield Token('RPAREN')
				case '.'|'0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
					yield self.generate_number()
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
					break
			
			number_str += self.current_char
			self.get_next_char()

		if number_str.startswith('.'):
			number_str = '0' + number_str
		if number_str.endswith('.'):
			number_str += '0'

		return Token('NUMBER', float(number_str))
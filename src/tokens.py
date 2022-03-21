from enum import Enum

class TokenType(Enum):
	INTEGER   = 0
	PLUS      = 1
	MINUS     = 2
	MULTIPLY  = 3
	DIVIDE    = 4
	LPAREN    = 5
	RPAREN    = 6
	EQUALS    = 7
	KEYWORD   = 8
	IDENTIFIER= 9
	EOF       = 10
	ASSIGN    = 11
	NOT       = 12
	LT        = 13
	AND       = 14
	RANGE     = 15
	STRING    = 16
	NEWLINE   = 17

class Token:
	def __init__(self, type, value=None, pos_start=None, pos_end=None):
		self.type = type
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end.copy()

	def matches(self, type_, value):
		return self.type == type_ and self.value == value

	def __repr__(self):
		return self.type.name + (f":{self.value}" if self.value != None else "")
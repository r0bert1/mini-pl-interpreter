expression --> term ((PLUS|MINUS) term)\* | KEYWORD:VAR IDENTIFIER EQUALS expression

term --> factor ((MUL|DIV) factor)\*

factor --> (PLUS|MINUS)\* NUMBER | LPAREN expression RPAREN

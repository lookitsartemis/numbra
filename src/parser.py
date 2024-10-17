import math

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        """Consume a token of the given type."""
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def assign(self):
        """assign : ID '=' expr"""
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('EQUALS') 
        value = self.expr()
        self.variables[var_name] = value
        return value

    def factor(self):
        """factor : NUMBER | ID | LPAREN expr RPAREN | FUNC LPAREN expr RPAREN"""
        if self.current_token[0] == 'FUNC':
            func_name = self.current_token[1]
            self.eat('FUNC')
            self.eat('LPAREN')
            arg = self.expr()
            self.eat('RPAREN')
            
            if func_name == 'sqrt':
                return math.sqrt(arg)
            elif func_name == 'sin':
                return math.sin(arg)
            elif func_name == 'cos':
                return math.cos(arg)
        elif self.current_token[0] == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
        elif self.current_token[0] == 'ID':
            var_name = self.current_token[1]
            self.eat('ID')
            return self.variables.get(var_name, 0)
        else:
            token = self.current_token
            self.eat('NUMBER')
            return token[1]

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()
        while self.current_token[0] in ('MUL', 'DIV'):
            token = self.current_token
            if token[0] == 'MUL':
                self.eat('MUL')
                result *= self.factor()
            elif token[0] == 'DIV':
                self.eat('DIV')
                result /= self.factor()
        return result

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        result = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            token = self.current_token
            if token[0] == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif token[0] == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        return result

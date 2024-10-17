import math

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        """Consume a token of the given type and advance to the next one."""
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : NUMBER | ID | LPAREN expr RPAREN | FUNC LPAREN expr RPAREN"""
        token = self.current_token
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return token[1]
        elif token[0] == 'ID':
            var_name = token[1]
            self.eat('ID')
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise Exception(f"Variable '{var_name}' is not defined")
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
        elif token[0] == 'FUNC':
            func_name = token[1]
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
        else:
            self.error()

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

    def assign(self):
        """assign : ID EQUALS expr"""
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('EQUALS')
        value = self.expr()
        self.variables[var_name] = value
        return value

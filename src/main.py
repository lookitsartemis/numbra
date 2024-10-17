from lexer import Lexer
from parser import Parser

def main():
    while True:
        try:
            text = input("Numbra> ")
            if text.strip() == "":
                continue
            
            lexer = Lexer(text)
            parser = Parser(lexer)

            if parser.current_token[0] == 'ID':
                next_token = lexer.get_next_token()
                if next_token[0] == 'EQUALS':
                    parser.current_token = next_token
                    result = parser.assign()
                else:
                    result = parser.expr()
            else:
                result = parser.expr()

            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

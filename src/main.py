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
            result = parser.expr()
            print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()

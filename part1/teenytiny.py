from lex import *

def main():
    inputs = input("Please enter some words:")#使用者輸入
    lexer = Lexer(inputs)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.getToken()

main()
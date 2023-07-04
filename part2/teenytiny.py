from lex import *
from parse import *
import sys

def main():
    print("Teeny Tiny Compiler")
    
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    comment=False#多行讀取
    with open(sys.argv[1], 'r') as inputFile:
      for line in inputFile.readlines():#依次讀行
        input=line  
        #input = inputFile.read()

        # Initialize the lexer and parser.
        lexer = Lexer(input,comment)
        parser = Parser(lexer)

        parser.program() # Start the parser.
    print("Parsing completed.")

main()
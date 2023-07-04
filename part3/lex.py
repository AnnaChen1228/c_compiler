import sys
import enum

# Lexer object keeps track of current position in the source code and produces each token.
class Lexer:
    def __init__(self, input,comment,gotolabel):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()
        self.comment=comment
        self.gotolabel=gotolabel
        self.pastChar = ''

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier, or keyword, then we will process the rest.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
                
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar=='%':#加上取餘數
            token=Token(self.curChar,TokenType.REMINDER)
        elif self.curChar == '=':
            # Check whether this token is = or ==
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            # Check whether this is token is > or >=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            # Check whether this is token is < or <=
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            elif self.peek()=='+':
                lastChar = '-'
                self.nextChar()
                token = Token(lastChar, TokenType.MINUS)
            elif self.peek()=='-':
                lastChar = '+'
                self.nextChar()
                token = Token(lastChar, TokenType.PLUS)
            elif self.peek()=='*':
                lastChar = '/'
                self.nextChar()
                token = Token(lastChar, TokenType.SLASH)
            elif self.peek()=='/':
                lastChar = '*'
                self.nextChar()
                token = Token(lastChar, TokenType.ASTERISK)
            elif self.peek() == '>':
                firstChar='<'
                self.nextChar()
                if self.peek() == '=':
                    self.nextChar()
                    token = Token(firstChar, TokenType.LT)
                else:
                    lastChar = '='
                    token = Token(firstChar+lastChar, TokenType.LTEQ)
            elif self.peek() == '<':
                firstChar='>'
                self.nextChar()
                if self.peek() == '=':
                    self.nextChar()
                    token = Token(firstChar, TokenType.GT)
                else:
                    lastChar = '='
                    token = Token(firstChar+lastChar, TokenType.GTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())

        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos] # Get the substring.
            token = Token(tokText, TokenType.STRING)

        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.': # Decimal!
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit(): 
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():#判別是否為字母
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numeric characters.
            startPos = self.curPos
            while self.peek().isalnum():#判別是否為數字或字母
                self.nextChar()

            # Check if the token is in the list of keywords.
            tokText = self.source[startPos : self.curPos + 1] # Get the substring.
            tokText=tokText.upper()#強制轉大寫
            keyword = Token.checkIfKeyword(tokText)
            if self.gotolabel==True:
                token = Token(tokText, TokenType.LABEL)
            elif keyword == None: # Identifier
                token = Token(tokText, TokenType.IDENT)
            else:   # Keyword
                token = Token(tokText, keyword)
                if keyword == TokenType.GOTO:
                    self.gotolabel=True

        elif self.curChar == '\n':
            # Newline.
            token = Token('\n', TokenType.NEWLINE)
        elif self.curChar == '\0':
             # EOF.
            token = Token('', TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.curChar)

        self.pastChar=self.curChar
        self.nextChar()
        
        return token

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        if self.comment==True:#當處於多行註解，尋找結束點
          while self.curChar != '\n' and self.curChar!='*'and self.peek()!='/':
            self.nextChar()
          #print(2)
          if self.curChar=='*'and self.peek()=='/':
            print(3)
            self.comment=False
            self.nextChar()
            self.nextChar()
          #while self.curChar != '\n':
                #self.nextChar()
        if self.curChar == '#'or (self.curChar=='/'and self.peek()=='/'):#判別屬於單行註解
            while self.curChar != '\n':
                self.nextChar()
        elif self.curChar=='/'and self.peek()=='*':#判別是否屬於多行註解
            print(1)
            self.comment=True
            while self.curChar != '\n':
                if self.curChar=='*'and self.peek()=='/':#用於單行
                    self.comment=False
                self.nextChar()


# Token contains the original text and the type of token.
class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    ELSE=112
    ENDELSE=113
    FOR=114
    ENDFOR=115
    MIN=116
    MAX=117
    SORT=118
    # Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    REMINDER = 212
"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - v class: 'class' className '{' classVarDec* subroutineDec* '}'
    - v classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_stream.read().splitlines()
        self.keywords = ["class", "constructor", "function",
                         "method", "field", "static", "var",
                         "int", "char", "boolean", "void", "true",
                         "false", "null", "this", "let", "do", "if",
                         "else", "while", "return"]
        self.symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";",
                        "+", "-", "*", "/", "&", "|", "<", ">", "=",
                        "~", "^", "#"]
        # declare Tokenizer input_lines
        self.input_lines = input_stream.read().strip().splitlines()
        # remove comments
        self.__remove_comments()
        # make a list of tokens/ some sort of iterator
        self.len = len(self.input_lines)
        # declare Tokenizer curs
        self.cur_index = 0
        self.cur = self.input_lines[0]

    def __remove_comments(self) -> None:
        # declare flags
        in_comment_block = False
        result = []
        # iterate over every line and every character
        for line in self.input_lines:
            line = line.strip()
            if not in_comment_block:
                # look for "/*" - start of comment block
                if "/*" in line:
                    in_comment_block = True
                    # look for comment close in same line
                    if "*/" in line:
                        in_comment_block = False
                        line = line[:line.index("/*")] + line[line.index("*/") + 2:]
                    # if closer not found remove everything from beginning of comment in line
                    else:
                        line = line[:line.index("/*")]
                # same as above for /**
                elif "/**" in line:
                    in_comment_block = True
                    if "*/" in line:
                        in_comment_block = False
                        line = line[:line.index("/*")] + line[line.index("*/") + 2:]
                    else:
                        line = line[:line.index("/*")]
                # look for "//" - if found, remove everything until the end of the line
                elif "//" in line:
                    line = line[:line.index("//")]
            # if comment closer not found in same line, it must be in another line
            else:
                if "*/" in line:
                    if line == "*/":
                        line = ""
                        in_comment_block = False
                    else:
                        in_comment_block = False
                        line = line[line.index("*/") + 2:]
                else:
                    line = ""

            if line.strip():
                words = re.findall(r'\w+|[{}()[\].,;+\-*/&|<>=~^#"?:]', line)
                result.extend(words)

        self.input_lines = result

    def get_look_ahead_token(self, k: int = 1):
        """Get a look ahead token at k steps"""
        if self.cur_index + k < self.len:
            return self.input_lines[self.cur_index + k - 1]

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        if self.cur_index < self.len:
            return True
        return False

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        self.cur = self.input_lines[self.cur_index]
        self.cur_index += 1
        pass

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        res = ""
        if self.cur in self.keywords:
            res = "KEYWORD"
        elif self.cur in self.symbols:
            res = "SYMBOL"
        elif self.cur.isdigit():
            res = "INT_CONST"
        elif self.cur == '"':
            res = "STRING_CONST"
        else:
            if not self.cur[0].isdigit():
                res = "IDENTIFIER"
            else:
                raise ValueError("Identifier cannot start with digit")
        return res

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.cur.upper()
        pass

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.cur
        pass

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.cur
        pass

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        if int(self.cur) > 32767:
            raise ValueError("Integer overflow")
        return int(self.cur)
        pass

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # assuming cur is currently on "
        self.advance()
        res = ""
        while self.cur != '"':
            res += self.cur + " "
            if self.has_more_tokens():
                self.advance()
            # TODO if no more tokens and end " not found, raise exception
            else:
                raise ValueError('Missing matching "')

        return res

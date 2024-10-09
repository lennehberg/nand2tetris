"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *


class CriticalError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]


#       super.__init__(self.message)


class NonCriticalError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]


#        super.__init__(self.message)


class KeywordError(Exception):
    def __int__(self, message):
        self.message = message
        # super.__init__(self.message)

    def message(self):
        return self.args[0]


class SymbolError(Exception):
    def __int__(self, message):
        self.message = message
        # super.__init__(self.message)

    def message(self):
        return self.args[0]


class IdentifierError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]
        # super.__init__(self.message)


class ConstantIntError(Exception):
    def __int__(self, message):
        self.message = message
        # super.__init__(self.message)

    def message(self):
        return self.args[0]


class ConstantStringError(Exception):
    def __int__(self, message):
        self.message = message
        # super.__init__(self.message)

    def message(self):
        return self.args[0]


class SubroutineError(Exception):
    def __int__(self, message):
        self.message = message
        # super.__init__(self.message)

    def message(self):
        return self.args[0]


class ArrayError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]


#        super.__init__(self.message)


class TokenizerError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]


#        super.__init__(self.message)


class CompilationError(Exception):
    def __int__(self, message):
        self.message = message

    def message(self):
        return self.args[0]


#       super.__init__(self.message)


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    #  sets a static list of class names
    s_class_list = ["Array"]
    sub_rout_list = []

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        # assuming that <tokens> was written in Analyzer
        self.tokenizer: JackTokenizer = input_stream
        self.out_stream = output_stream
        if not self.tokenizer.has_more_tokens():
            raise CriticalError("Empty file")
        # self.out_stream.write("<tokens>\n")
        pass

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # assuming the need for a jack file to start
        # with the keyword "class"
        # write class to out file
        self.out_stream.write("<class>\n")
        self.tokenizer.advance()
        self.__write_keyword("CLASS")
        self.__check_tokenizer()
        # write identifier
        self.tokenizer.advance()
        self.__write_identifier()
        # add class identifier to s_class
        self.s_class_list.append(self.tokenizer.identifier())
        self.__check_tokenizer()
        # write {
        self.tokenizer.advance()
        self.__write_symbol("{")
        self.__check_tokenizer()
        # do class_var_dec subroutine - could have no var decs
        self.tokenizer.advance()
        try:
            self.compile_class_var_dec()
        except CriticalError as critical:
            raise critical
        except NonCriticalError:
            pass
        finally:
            # do compile_subroutine
            self.compile_subroutine()
            self.__write_symbol("}")
            self.out_stream.write("</class>\n")
            # finished

    def __write_keyword(self, expected) -> None:
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() in expected:
                self.out_stream.write(f"<keyword> {self.tokenizer.keyword().lower()} </keyword>\n")
            else:
                raise KeywordError(f"Expected keyword {expected}")
        else:
            raise KeywordError("Expected keyword")

    def __write_identifier(self) -> None:
        if self.tokenizer.token_type() == "IDENTIFIER":
            self.out_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>\n")
        else:
            raise IdentifierError("Expected identifier")

    def __check_tokenizer(self) -> None:
        if not self.tokenizer.has_more_tokens():
            raise TokenizerError("Expected more tokens")

    def __write_symbol(self, expected):
        special = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;"
        }
        if self.tokenizer.token_type() == "SYMBOL":
            if self.tokenizer.symbol() in expected:
                self.out_stream.write(f"<symbol> "
                                      f"{self.tokenizer.symbol() if self.tokenizer.symbol() not in special else special[self.tokenizer.symbol()]}"
                                      f" </symbol>\n")
            else:
                raise SymbolError(f"Expected symbol {expected}")
        else:
            raise SymbolError("Expected symbol")

    def compile_class_var_dec(self) -> None:

        # declare list of var types
        class_vars = ["FIELD", "STATIC"]
        # error handling by parent
        # while tokenizer has more tokens
        while self.tokenizer.has_more_tokens():
            # try to compile var dec for class
            try:
                if self.tokenizer.token_type() == "KEYWORD":
                    if self.tokenizer.keyword() == "FIELD" or self.tokenizer.keyword() == "STATIC":
                        self.out_stream.write("<classVarDec>\n")
                # write class vars type
                self.__write_keyword(class_vars)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write type of var
                self.__write_var_type()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # try to write var list subroutine
                self.var_list_routine()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.out_stream.write("</classVarDec>\n")
            except CriticalError as critical:
                raise critical
            except KeywordError:
                raise NonCriticalError
            except NonCriticalError:
                pass
            except IdentifierError as identifier:
                raise identifier

    def var_list_routine(self) -> None:
        """tries to write a var list until ; is met, raises appropriate errors"""
        no_semi = True
        try:
            while no_semi:
                # write identifier
                self.__write_identifier()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.__write_symbol(",")
                self.__check_tokenizer()
                self.tokenizer.advance()
        except SymbolError:
            try:
                self.__write_symbol(";")
            except SymbolError:
                raise CriticalError("Expected , or ;")

    # def compile_class_var_dec(self) -> None:
    #     """Compiles a static declaration or a field declaration."""
    #     # Your code goes here!
    #
    #     # assume tokenizer in correct position
    #     # set a types list
    #     # check if statement begins in a static of field declaration
    #     # and if there are any more than 1 (while loop)
    #     while self.tokenizer.has_more_tokens():
    #         # try write keyword static or field
    #         try:
    #             self.__write_keyword("FIELD")
    #         except KeywordError:
    #             try:
    #                 self.__write_keyword("STATIC")
    #             except KeywordError:
    #                 raise NonCriticalError("class doesnt need vars")
    #
    #         self.__check_tokenizer()
    #         self.tokenizer.advance()
    #         # try write keyword type
    #         try:
    #             self.__write_var_type()  # self.__write_keyword(types)
    #         except CriticalError as critical:
    #             raise critical
    #
    #         self.__check_tokenizer()
    #         self.tokenizer.advance()
    #         # write varName identifier
    #         self.__write_var_name()
    #         self.__check_tokenizer()
    #         self.tokenizer.advance()
    #         # try write symbol comma
    #         try:
    #             self.__write_symbol(",")
    #             self.__check_tokenizer()
    #             self.tokenizer.advance()
    #             no_semi = True
    #             while no_semi:
    #                 # if success, go continue loop of writing varName identifier
    #                 # trying to write comma or semicolon
    #                 self.__write_identifier()
    #                 self.__check_tokenizer()
    #                 self.tokenizer.advance()
    #                 try:
    #                     self.__write_symbol(";")
    #                     # self.__check_tokenizer()
    #                     # self.tokenizer.advance()
    #                     no_semi = False
    #                 except ValueError:
    #                     self.__write_symbol(",")
    #                 self.__check_tokenizer()
    #                 self.tokenizer.advance()
    #         # except write symbol ;
    #         except ValueError:
    #             self.__write_symbol(";")
    #             self.__check_tokenizer()
    #             self.tokenizer.advance()

    def __write_class_name_keyword(self):
        if self.tokenizer.token_type() == "IDENTIFIER":
            # if self.tokenizer.identifier() in self.s_class_list:
            self.out_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>\n")
            # else:
            #   raise ValueError("Expected type")
        else:
            raise IdentifierError("Expected type")

    def compile_subroutine(self) -> None:
        """
            Compiles a complete method, function, or constructor.
            You can assume that classes with constructors have at least one field,
            you will understand why this is necessary in project 11.
            """
        # Your code goes here!

        sub_decs = ["FUNCTION", "METHOD", "CONSTRUCTOR"]
        sub_types = ["INT", "BOOLEAN", "CHAR", "VOID"]
        # while token has more tokens
        while self.tokenizer.has_more_tokens() and not self.__check_closer("}"):
            # write function/method/contructor keyword
            try:
                self.out_stream.write("<subroutineDec>\n")
                self.__write_keyword(sub_decs)
                # if not subroutine keyword, break
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write subtype keyword
                self.__write_var_type(sub_types)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write subroutine identifier, add to subroutines list
                self.__write_identifier()
                self.sub_rout_list.append(self.tokenizer.identifier())
                self.__check_tokenizer()
                self.tokenizer.advance()
                # find ( token
                self.__write_symbol("(")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write parameter list -
                # already advances tokenizer to )
                self.compile_parameter_list()
                # find ) token
                self.__write_symbol(")")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # find } token
                # self.__write_symbol("{")
                # self.__check_tokenizer()
                # self.tokenizer.advance()
                # write subroutine body
                self.compile_subroutine_body()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.out_stream.write("</subroutineDec>\n")
            except KeywordError:
                pass
            except CriticalError as critical:
                raise critical
            except IdentifierError as identifier:
                raise identifier
            except SymbolError as symbol:
                raise symbol

    # def compile_subroutine(self) -> None:
    #     """
    #     Compiles a complete method, function, or constructor.
    #     You can assume that classes with constructors have at least one field,
    #     you will understand why this is necessary in project 11.
    #     """
    #     # Your code goes here!
    #     sub_decs = ["FUNCTION", "METHOD", "CONSTRUCTOR"]
    #     sub_types = ["INT", "BOOLEAN", "CHAR", "VOID"]
    # while token has more tokens
    # while self.tokenizer.has_more_tokens() and not self.__check_closer("}"):
    #     # write function/method/contructor keyword
    #     try:
    #         self.__write_keyword(sub_decs)
    #     # if not subroutine keyword, break
    #     except ValueError:
    #         break
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # write subtype keyword
    #     try:
    #         self.__write_keyword(sub_types)
    #     except ValueError:
    #         self.__write_class_name_keyword()
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # write subroutine identifier, add to subroutines list
    #     self.__write_identifier()
    #     self.sub_rout_list.append(self.tokenizer.identifier())
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # find ( token
    #     self.__write_symbol("(")
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # write parameter list -
    #     # already advances tokenizer to )
    #     self.compile_parameter_list()
    #     # find ) token
    #     self.__write_symbol(")")
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # find } token
    #     self.__write_symbol("{")
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()
    #     # write subroutine body
    #     self.compile_subroutine_body()
    #     self.__check_tokenizer()
    #     self.tokenizer.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        # while tokenzier has more tokens
        self.out_stream.write("<parameterList>\n")
        while self.tokenizer.has_more_tokens() and not self.__check_closer(")"):
            # try to write type
            try:
                self.__write_var_type()

                self.__check_tokenizer()
                self.tokenizer.advance()
                self.__write_var_name()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # try write comma symbol
                self.__write_symbol(",")

                self.__check_tokenizer()
                self.tokenizer.advance()
            # if fail, break
            except CriticalError as critical:
                raise critical
            except NonCriticalError:
                break
            except SymbolError:
                break
            except IdentifierError as identifier:
                raise identifier
        self.out_stream.write("</parameterList>\n")

    def __write_var_type(self, types=("INT", "CHAR", "BOOLEAN")) -> None:
        """Writes the type of something according to types"""
        # write type keyword
        try:
            self.__write_keyword(types)
        except KeywordError:
            # write className variable
            self.__write_class_name_keyword()
        except IdentifierError:
            raise CriticalError("Expected var type")

    def __write_var_name(self) -> None:
        """writes the name of var with the type,
        assuming tokenizer in correct position,
        doesn't advance identifier """
        self.__write_identifier()

    def __check_closer(self, expected_finisher) -> bool:
        if self.tokenizer.token_type() == "SYMBOL":
            if self.tokenizer.symbol() == expected_finisher:
                return True
        return False

    def compile_subroutine_body(self) -> None:
        """decides what needs to be compiled for subroutine body"""
        self.out_stream.write("<subroutineBody>\n")
        self.__write_symbol("{")
        self.__check_tokenizer()
        self.tokenizer.advance()
        # while has more token
        while self.tokenizer.has_more_tokens() and not self.__check_closer("}"):
            # try to compile var declarations
            try:

                self.compile_var_dec()

                if self.__check_closer("}"):
                    break
                self.__check_tokenizer()
                self.tokenizer.advance()
            except KeywordError:
                # compile statements
                self.out_stream.write("<statements>\n")
                self.compile_statements()
                self.out_stream.write("</statements>\n")
                if self.__check_closer("}"):
                    break
                self.__check_tokenizer()
                self.tokenizer.advance()
            except IdentifierError as identifier:
                raise CriticalError(identifier.message())
            except CriticalError as critical:
                raise critical
        self.__write_symbol("}")
        self.out_stream.write("</subroutineBody>\n")
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        # write var keyword
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "VAR":
                self.out_stream.write("<varDec>\n")
        self.__write_keyword("VAR")
        self.__check_tokenizer()
        self.tokenizer.advance()
        # write type keyword
        self.__write_var_type()
        self.__check_tokenizer()
        self.tokenizer.advance()
        # write varName
        self.__write_var_name()
        self.__check_tokenizer()
        self.tokenizer.advance()
        # try write symbol comma
        try:
            self.__write_symbol(",")
            self.__check_tokenizer()
            self.tokenizer.advance()
            no_semi = True
            while no_semi:
                # if success, go continue loop of writing varName identifier
                # trying to write comma or semicolon
                self.__write_identifier()
                self.__check_tokenizer()
                self.tokenizer.advance()
                try:
                    self.__write_symbol(";")
                    no_semi = False
                except SymbolError:
                    self.__write_symbol(",")
        # except write symbol ;
        except SymbolError:
            self.__write_symbol(";")
        except KeywordError as keyword:
            raise CriticalError(keyword.message())
        except CompilationError as compilation:
            raise CriticalError(compilation.message())
        self.out_stream.write("</varDec>\n")
        pass

    @staticmethod
    def comp_arr_it(compile_arr, error_arr) -> bool:
        """Iterates over array of compilation functions,
        return true if compilation successful, false otherwise"""
        compiled = False
        # iterate over function array
        for i in range(len(compile_arr)):
            # if no compilation has yet to succeed
            if not compiled:
                # try to compile and set true
                try:
                    compile_arr[i]()
                    compiled = True
                # else save error in error array and continue
                except NonCriticalError:
                    continue
                except CriticalError as e:
                    error_arr.insert(i, str(e))
        return compiled

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        # save function in array, declare new errors array
        compile_arr = [self.compile_do, self.compile_let, self.compile_while,
                       self.compile_if, self.compile_return]
        error_arr = ["" for _ in range(len(compile_arr))]
        compiled = False
        had_tokens = False
        # while has more tokens and token not finisher
        while self.tokenizer.has_more_tokens() and not self.__check_closer("}"):
            had_tokens = True
            # reset error arr for new statement compilation
            error_arr = ["" for _ in range(len(compile_arr))]
            compiled = self.comp_arr_it(compile_arr, error_arr)
            # go to next statement if after ; closer
            if not self.__check_closer(";"):
                continue
            # if successfully compiled a statement, advance tokenizer
            if compiled:
                self.__check_tokenizer()
                self.tokenizer.advance()
            # else. break
            else:
                break

        # if no compilation succeeded,
        if not compiled:
            # raise all errors in error array
            # only if entered while
            if had_tokens:
                error_msg = ""
                for i in range(len(compile_arr)):
                    error_msg += error_arr[i] + "\n"
                raise CriticalError(error_msg)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        # write keyword do
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "DO":
                self.out_stream.write("<doStatement>\n")
        try:
            self.__write_keyword("DO")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write subroutine name
            self.compile_subroutine_term()
            # check subroutine name in declared subroutines
            # if not self.tokenizer.identifier() in self.sub_rout_list:
            #     raise ValueError("Invalid call")
            # write symbol ;
            self.__check_tokenizer()
            self.tokenizer.advance()
            self.__write_symbol(";")
        except KeywordError:
            raise NonCriticalError("Not do")
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())
        self.out_stream.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "LET":
                self.out_stream.write("<letStatement>\n")
        try:
            # write the let keyword
            self.__write_keyword("LET")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write varName
            self.__write_var_name()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # try to write [
            try:
                self.__write_symbol("[")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # if successfull, write expression
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write ]
                self.__write_symbol("]")
                self.__check_tokenizer()
                self.tokenizer.advance()
            except SymbolError:
                pass
            except CriticalError as critical:
                raise critical
            finally:
                # write symbol =
                self.__write_symbol("=")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write expression
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write symbol ;
                self.__write_symbol(";")
                self.out_stream.write("</letStatement>\n")
        except KeywordError:
            raise NonCriticalError("Not let")
        except IdentifierError as identifier:
            raise CriticalError(identifier.message())

    def compile_while(self) -> None:
        """Compiles a while statement."""
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "WHILE":
                self.out_stream.write("<whileStatement>\n")
        # Your code goes here!
        try:
            # write while
            self.__write_keyword("WHILE")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write (
            self.__write_symbol("(")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write expression
            self.compile_expression()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write )
            self.__write_symbol(")")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write {
            self.__write_symbol("{")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write statements
            self.out_stream.write("<statements>\n")
            self.compile_statements()
            self.out_stream.write("</statements>\n")
            # write }
            self.__write_symbol("}")
            # TODO TEST
            self.__check_tokenizer()
            self.tokenizer.advance()
            self.out_stream.write("</whileStatement>\n")
        except KeywordError:
            raise NonCriticalError("Not while")
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "RETURN":
                self.out_stream.write("<returnStatement>\n")
        try:
            # write return keyword
            self.__write_keyword("RETURN")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # try write expression
            try:
                if not self.__check_closer(";"):
                    self.compile_expression()
                    self.__check_tokenizer()
                    self.tokenizer.advance()
            except CriticalError:
                pass
            # finally write symbol ;
            finally:
                self.__write_symbol(";")
                self.out_stream.write("</returnStatement>\n")
        except KeywordError:
            raise NonCriticalError("Not return")
        except SymbolError as symbol:
            raise CriticalError(symbol.message())

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        has_if_s = False
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "IF":
                self.out_stream.write("<ifStatement>\n")
        try:
            # write if keyword
            self.__write_keyword("IF")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write (
            self.__write_symbol("(")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write expression
            self.compile_expression()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write )
            self.__write_symbol(")")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write {
            self.__write_symbol("{")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write statements - moves cur to {
            self.out_stream.write("<statements>\n")
            self.compile_statements()
            self.out_stream.write("</statements>\n")
            # write }
            self.__write_symbol("}")
            self.__check_tokenizer()
            self.tokenizer.advance()
            has_if_s = True
            # try write else
            self.__write_keyword("ELSE")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write {
            self.__write_symbol("{")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write statements
            self.out_stream.write("<statements>\n")
            self.compile_statements()
            self.out_stream.write("</statements>\n")
            # write }
            self.__write_symbol("}")
            self.__check_tokenizer()
            self.tokenizer.advance()
        except KeywordError:
            if has_if_s:
                self.out_stream.write("</ifStatement>\n")
            raise NonCriticalError("Not if/else")
        except SymbolError as symbol:
            raise CriticalError(symbol.message())
        except CriticalError as critical:
            raise critical

        self.out_stream.write("</ifStatement>\n")

    # TODO continue handling errors
    def compile_expression(self, new=True) -> None:
        """Compiles an expression."""
        if new:
            self.out_stream.write("<expression>\n")
        # Your code goes here!
        ops = ["+", "-", "*", "/",
               "&", "|", "<", ">",
               "="]

        try:
            # compile term
            self.out_stream.write("<term>\n")
            self.compile_term()
            self.out_stream.write("</term>\n")
            # try to write op symbol
            peak = self.tokenizer.get_look_ahead_token()
            if peak in ops:
                self.tokenizer.advance()
                self.__write_symbol(ops)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # compile expression
                self.compile_expression(False)
        # CriticalError- coming from compile term or compile expression
        except CriticalError as critical:
            raise critical
        # SymbolError- coming from potential op
        except SymbolError:
            pass
        if new:
            self.out_stream.write("</expression>\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        # try compile integerConstant/ stringConstant/ keywordConstant/
        #             array/ subroutineCall/ expression in parentheses/
        #             unaryOp term
        compile_arr = [self.compile_integer_term, self.compile_string_term,
                       self.compile_keyword_term, self.compile_array_addressing,
                       self.compile_subroutine_term, self.compile_paren_expression_term,
                       self.compile_unary_term, self.__write_var_name]
        error_arr = ["" for _ in range(len(compile_arr))]
        compiled = self.comp_arr_it(compile_arr, error_arr)

        if not compiled:
            error_msg = ""
            for i in range(len(compile_arr)):
                error_msg += error_arr[i] + "\n"
            raise CriticalError(error_msg)

    def compile_integer_term(self) -> None:
        """Tries to compile a term that is an integerConstant"""
        # check if token is INT_CONST
        if self.tokenizer.token_type() == "INT_CONST":
            # write integerConstant to file
            self.out_stream.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>\n")
        else:
            raise NonCriticalError("Not integerConstant")

    def compile_string_term(self) -> None:
        """tries to compile a term that is a stringConstant"""
        # check if token is STRING_CONST
        if self.tokenizer.token_type() == "STRING_CONST":
            # write stringConstant to file
            str_const = self.tokenizer.string_val()
            self.out_stream.write(f"<stringConstant> {str_const} </stringConstant>\n")
        else:
            raise NonCriticalError("Not stringConstant")

    def compile_keyword_term(self) -> None:
        """Tries to compile a term that is a keywordConstant"""
        # try to write keyword token
        # from the subset ["THIS", "NULL", "TRUE", "FALSE"]
        keyword_constants = ["THIS", "NULL", "TRUE", "FALSE"]
        try:
            self.__write_keyword(keyword_constants)
        except KeywordError:
            raise NonCriticalError("Not KeywordConstant")

    def compile_array_addressing(self) -> None:
        """Tries to compile a term that is an addressing to an array"""
        # check if look ahead token is [
        peak = self.tokenizer.get_look_ahead_token()
        if peak == "[":
            # write varName
            try:
                self.__write_var_name()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write [
                self.__write_symbol("[")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write expression
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write ]
                self.__write_symbol("]")
            except IdentifierError as identifier:
                raise CriticalError(identifier.message())
            except SymbolError as symbol:
                raise CriticalError(symbol)
            except CriticalError as critical:
                raise critical
        else:
            raise NonCriticalError("Not array addressing")

    def __write_generic_subroutine(self) -> None:
        """writes the generic subroutine call"""
        try:
            # write subroutine name
            self.__write_identifier()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write (
            self.__write_symbol("(")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write expressionList - can be empty
            self.compile_expression_list()
            # write )
            self.__write_symbol(")")
        except IdentifierError as identifier:
            raise CriticalError(identifier.message())
        except SymbolError as symbol:
            raise CriticalError(symbol)
        except CriticalError as critical:
            raise critical
        except NonCriticalError:
            pass

    def compile_subroutine_term(self) -> None:
        """Tries to compile a term that is a call to a subroutine"""
        # if look ahead token is (, compile subroutineCall
        peak = self.tokenizer.get_look_ahead_token()
        try:
            if peak == "(":
                self.__write_generic_subroutine()
            # if look-ahead token is ., subroutine call will come from class name
            elif peak == ".":
                try:
                    self.__write_var_name()
                except IdentifierError:
                    self.__write_class_name_keyword()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.__write_symbol(".")
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.compile_subroutine_term()
            else:
                raise SubroutineError("Not subroutineCall")
        except CriticalError as critical:
            raise critical
        except SubroutineError:
            raise NonCriticalError("Not subroutine")
        except IdentifierError as identifier:
            raise CriticalError(identifier.message())
        except SymbolError as symbol:
            raise CriticalError(symbol.message())

    def compile_paren_expression_term(self) -> None:
        """Tries to write an expression in parentheses"""
        # write (
        try:
            self.__write_symbol("(")
        except SymbolError:
            raise NonCriticalError("Not an expression in parentheses")
        try:
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write expression
            self.compile_expression()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write )
            self.__write_symbol(")")
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())

    def compile_unary_term(self) -> None:
        """Tries to write a unary operator followed by a term"""
        # write unaryOp
        unary_ops = ["-", "~", "^", "#"]
        try:
            self.__write_symbol(unary_ops)
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write term
            self.out_stream.write("<term>\n")
            self.compile_term()
            self.out_stream.write("</term>\n")
        except CriticalError as critical:
            raise critical
        except SymbolError:
            raise NonCriticalError("Not unary op")

    def compile_expression_list(self, new=True) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        # try to compile expression
        if new:
            self.out_stream.write("<expressionList>\n")
        try:
            if not self.__check_closer(")"):
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
            # try to write comma symbol
            self.__write_symbol(",")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # call compile_expression_list
            self.compile_expression_list(False)
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())
        except NonCriticalError:
            return
        # finally, could be empty, return
        finally:
            if new:
                self.out_stream.write("</expressionList>\n")
            return

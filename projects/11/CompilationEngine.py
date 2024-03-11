"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import *
from SymbolTable import *
from VMWriter import *
import os


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

    # declare a static label counter
    label_counter: int = 0

    def __init__(self, input_stream: JackTokenizer, symbol_table: SymbolTable, writer: VMWriter, output_stream) -> None:
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
        self.sym_table: SymbolTable = symbol_table
        self.writer = writer
        if not self.tokenizer.has_more_tokens():
            raise CriticalError("Empty file")
        # self.out_stream.write("<tokens>\n")
        pass

    """ HELPERS """

    @staticmethod
    def __get_xml_vm(filepath: str) -> tuple:
        base, ext = os.path.splitext(filepath)
        if ext == ".vm":
            ext = ".xml"
            new_filepath = base + ext
            return new_filepath, filepath
        else:
            ext = ".vm"
            new_filepath = base + ext
            return filepath, new_filepath

    def __generate_label(self, statement) -> str:
        label = statement + f".{self.label_counter}"
        self.label_counter += 1
        return label

    def __write_keyword(self, expected) -> str:
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() in expected:
                self.out_stream.write(f"<keyword> {self.tokenizer.keyword().lower()} </keyword>\n")
                return self.tokenizer.keyword()
            else:
                raise KeywordError(f"Expected keyword {expected}")
        else:
            raise KeywordError("Expected keyword")

    def __write_identifier(self, type="", kind="") -> str:
        """writes the indentifier, adds to symbol table"""
        if self.tokenizer.token_type() == "IDENTIFIER":
            if not (type == "" or kind == ""):
                self.sym_table.define(self.tokenizer.identifier(), type, kind)
                self.out_stream.write(
                    f"<{type}.{kind}.{self.sym_table.index_of(self.tokenizer.identifier())}.identifier> "
                    f"{self.tokenizer.identifier()} "
                    f"</{type}.{kind}.identifier>\n")
            else:
                self.out_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>\n")
            return self.tokenizer.identifier()
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

    def __write_class_name_keyword(self):
        if self.tokenizer.token_type() == "IDENTIFIER":
            # if self.tokenizer.identifier() in self.s_class_list:
            self.out_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>\n")
            return self.tokenizer.identifier()
            # else:
            #   raise ValueError("Expected type")
        else:
            raise IdentifierError("Expected type")

    def __write_var_type(self, types=("INT", "CHAR", "BOOLEAN")) -> str:
        """Writes the type of something according to types"""
        type: str = ""
        # write type keyword
        try:
            type = self.__write_keyword(types)
        except KeywordError:
            # write className variable
            type = self.__write_class_name_keyword()
        except IdentifierError:
            raise CriticalError("Expected var type")
        return type

    def __write_var_and_push(self, type="", kind=""):
        self.__write_var_name(type, kind, True)

    def __write_var_name(self, type="", kind="", push=False) -> str:
        """writes the name of var with the type,
        assuming tokenizer in correct position,
        doesn't advance identifier """
        # write push to vm if needed
        ident = self.__write_identifier(type, kind)
        if push:
            if self.sym_table.search_in_cur_scope(ident):
                self.writer.write_push(self.sym_table.kind_of(ident), self.sym_table.index_of(ident))
            elif self.sym_table.search_in_out_outer(ident):
                self.writer.write_push(self.sym_table.outer_kind_of(ident), self.sym_table.outer_index_of(ident))
        return ident

    def __check_closer(self, expected_finisher) -> bool:
        if self.tokenizer.token_type() == "SYMBOL":
            if self.tokenizer.symbol() == expected_finisher:
                return True
        return False

    def __generate_comment(self, expected_finisher) -> str:
        counter = 0
        msg: str = ""
        peak = self.tokenizer.get_look_ahead_token(counter)
        while not peak == expected_finisher:
            msg += peak + " "
            counter += 1
            peak = self.tokenizer.get_look_ahead_token(counter)
        return msg

    """ METHODS """

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
        self.__write_identifier("", "")
        name = self.tokenizer.identifier()
        # add class identifier to s_class

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
            # write function n_locals in vm
            # self.writer.write_function(name, self.sym_table.var_count("FIELD"))
            # do compile_subroutine
            self.compile_subroutine(name)

            self.__write_symbol("}")
            self.out_stream.write("</class>\n")
            # finished

    def compile_class_var_dec(self) -> None:
        """compiles declaration of class variables"""
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
                kind = self.__write_keyword(class_vars)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write type of var
                type = self.__write_var_type()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # try to write var list subroutine
                self.var_list_routine(type, kind)
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

    def var_list_routine(self, type, kind) -> None:
        """tries to write a var list until ; is met, raises appropriate errors"""
        no_semi = True
        try:
            while no_semi:
                # write identifier
                self.__write_identifier(type, kind)
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

    def compile_subroutine(self, class_name) -> None:
        """
            Compiles a complete method, function, or constructor.
            You can assume that classes with constructors have at least one field,
            you will understand why this is necessary in project 11.
            """
        sub_decs = ["FUNCTION", "METHOD", "CONSTRUCTOR"]
        sub_types = ["INT", "BOOLEAN", "CHAR", "VOID"]
        # while token has more tokens
        while self.tokenizer.has_more_tokens() and not self.__check_closer("}"):
            # write function/method/contructor keyword
            try:
                self.out_stream.write("<subroutineDec>\n")
                # if not subroutine keyword, break
                kind = self.__write_keyword(sub_decs)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write subtype keyword
                type = self.__write_var_type(sub_types)
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write subroutine identifier, add to subroutines list
                self.__write_identifier(type, kind)
                name = self.tokenizer.identifier()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # find ( token
                self.__write_symbol("(")
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write parameter list -
                # already advances tokenizer to )
                self.sym_table.start_subroutine()
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
                self.compile_subroutine_body(f"{class_name}.{name}", kind)
                self.sym_table.end_subroutine()
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
                type = self.__write_var_type()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.__write_var_name(type, "ARG")
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

    def __alloc_constructor(self) -> None:
        field_count = self.sym_table.outer_var_count("FIELD")
        self.writer.write_push("constant", field_count)
        self.writer.write_call("Memory.alloc", 1)
        self.writer.write_pop("pointer", 0)

    def __align_this(self) -> None:
        self.writer.write_push("argument", 0)
        self.writer.write_pop("pointer", 0)

    def compile_subroutine_body(self, sub_name, sub_kind) -> None:
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
                    # write function in vm
                    self.writer.write_function(sub_name, self.sym_table.var_count("LOCAL"))
                    # if constructor function, write memory allocation
                    if sub_kind == "CONSTRUCTOR":
                        self.__alloc_constructor()
                    # else if method function, pop align THIS
                    elif sub_kind == "METHOD":
                        self.__align_this()
                    break
                self.__check_tokenizer()
                self.tokenizer.advance()
            except KeywordError:
                # write function in vm
                self.writer.write_function(sub_name, self.sym_table.var_count("LOCAL"))
                # if constructor function, write memory allocation
                if sub_kind == "CONSTRUCTOR":
                    self.__alloc_constructor()
                # else if method function, pop align THIS
                elif sub_kind == "METHOD":
                    self.__align_this()
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
        kind = self.__write_keyword("VAR")
        self.__check_tokenizer()
        self.tokenizer.advance()
        # write type keyword
        type = self.__write_var_type()
        self.__check_tokenizer()
        self.tokenizer.advance()
        # write varName
        self.__write_var_name(type, kind)
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
                self.__write_identifier(type, kind)
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

    def __get_function_name(self) -> str:
        """returns the name of the current do function"""
        peak = self.tokenizer.get_look_ahead_token()
        if peak == "(":
            return self.tokenizer.identifier()
        elif peak == ".":
            return f"{self.tokenizer.identifier()}.{self.tokenizer.get_look_ahead_token(2)}"

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
            # write comment for debugging
            comment = self.__generate_comment(";")
            self.writer.write_comment(comment)
            self.tokenizer.advance()
            # write subroutine name
            callee = self.__get_function_name()
            self.sym_table.add_func_dec(callee)
            n_args = self.compile_subroutine_term()
            # check subroutine name in declared subroutines
            # if not self.tokenizer.identifier() in self.sub_rout_list:
            #     raise ValueError("Invalid call")
            # write symbol ;
            self.__check_tokenizer()
            self.tokenizer.advance()
            self.__write_symbol(";")
            self.writer.write_pop("temp", 0)
            # write function call
            # self.writer.write_call(callee, n_args)
        except KeywordError:
            raise NonCriticalError("Not do")
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())
        self.out_stream.write("</doStatement>\n")

    def __push_var(self, name: str) -> None:
        """tries to push a varName, by searching it in the sym table"""
        if self.sym_table.search_in_cur_scope(name):
            self.writer.write_push(self.sym_table.kind_of(name), self.sym_table.index_of(name))
        elif self.sym_table.search_in_out_outer(name):
            self.writer.write_push(self.sym_table.outer_kind_of(name), self.sym_table.outer_index_of(name))

    def __pop_var(self, name: str) -> None:
        """tries to pop a varName, searching for it in sym table"""
        if self.sym_table.search_in_cur_scope(name):
            self.writer.write_pop(self.sym_table.kind_of(name), self.sym_table.index_of(name))
        elif self.sym_table.search_in_out_outer(name):
            self.writer.write_pop(self.sym_table.outer_kind_of(name), self.sym_table.outer_index_of(name))

    def compile_let(self) -> None:
        """Compiles a let statement."""
        let_arr = False
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "LET":
                self.out_stream.write("<letStatement>\n")
        try:
            # write the let keyword
            self.__write_keyword("LET")
            comment = self.__generate_comment(";")
            self.writer.write_comment(comment)
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write varName
            name = self.__write_var_name()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # try to write [
            try:
                self.__write_symbol("[")
                self.__check_tokenizer()
                let_arr = True
                # push var
                self.__push_var(name)
                self.tokenizer.advance()
                # if successfull, write expression
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # write ]
                self.__write_symbol("]")
                self.__check_tokenizer()
                self.writer.write_arithmetic("+")
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
                # at end of expression, value at top of stack,
                # pop to appropriate location on RAM
                if not let_arr:
                    self.__pop_var(name)
                else:
                    self.writer.write_pop("temp", 0)
                    self.writer.write_pop("pointer", 1)
                    self.writer.write_push("temp", 0)
                    self.writer.write_pop("that", 0)
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
            comment = self.__generate_comment("{")
            self.writer.write_comment(comment)
            label = self.__generate_label("WHILE")
            # write label to vm
            self.writer.write_label(label)
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
            self.writer.write_arithmetic("~")
            self.tokenizer.advance()
            # write if-goto end label
            end_label = "END_" + label
            self.writer.write_if(end_label)
            # write {
            self.__write_symbol("{")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write statements
            self.out_stream.write("<statements>\n")
            self.compile_statements()
            self.out_stream.write("</statements>\n")
            # write goto label
            self.writer.write_goto(label)
            # write }
            self.__write_symbol("}")
            # write end label
            self.writer.write_label(end_label)
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
        has_statement = False
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "RETURN":
                self.out_stream.write("<returnStatement>\n")
        try:
            # write return keyword
            self.__write_keyword("RETURN")
            comment = self.__generate_comment(";")
            self.writer.write_comment(comment)
            self.__check_tokenizer()
            self.tokenizer.advance()
            # try write expression
            try:
                if not self.__check_closer(";"):
                    has_statement = True
                    self.compile_expression()
                    self.__check_tokenizer()
                    self.tokenizer.advance()
            except CriticalError:
                pass
            # finally write symbol ;
            finally:
                # write vm return
                self.writer.write_return(has_statement)
                self.__write_symbol(";")
                self.out_stream.write("</returnStatement>\n")
        except KeywordError:
            raise NonCriticalError("Not return")
        except SymbolError as symbol:
            raise CriticalError(symbol.message())

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        # generate if label and write to vm
        if_label = self.__generate_label("IF")
        end_label = "END_" + if_label
        else_label = "ELSE_" + if_label
        has_if_s = False
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "IF":
                self.out_stream.write("<ifStatement>\n")
        try:
            # write if keyword
            self.__write_keyword("IF")
            comment = self.__generate_comment("{")
            self.writer.write_comment(comment)
            # self.writer.write_label(if_label)
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
            self.writer.write_arithmetic("~")
            self.__check_tokenizer()
            # write if-goto in vm
            self.writer.write_if(else_label)
            # self.writer.write_goto(else_label)
            self.tokenizer.advance()
            # write {
            self.__write_symbol("{")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write statements - moves cur to {
            self.out_stream.write("<statements>\n")
            self.compile_statements()
            self.out_stream.write("</statements>\n")
            # write goto end_label
            self.writer.write_goto(end_label)
            # write }
            self.__write_symbol("}")
            # write the else label
            self.writer.write_label(else_label)
            self.__check_tokenizer()
            self.tokenizer.advance()
            has_if_s = True
            # try write else
            self.__write_keyword("ELSE")
            comment = self.__generate_comment("{")
            self.writer.write_comment(comment)
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
            self.writer.write_label(end_label)
            self.tokenizer.advance()
        except KeywordError:
            if has_if_s:
                self.out_stream.write("</ifStatement>\n")
                self.writer.write_label(end_label)
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
                op = self.tokenizer.symbol()
                self.__check_tokenizer()
                self.tokenizer.advance()
                # compile expression
                self.compile_expression(False)
                # write operator (postfix notations)
                self.writer.write_arithmetic(op)
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
                       self.compile_unary_term, self.__write_var_and_push]
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
            # push constant <integerConstant> onto stack
            self.writer.write_push("CONST", self.tokenizer.int_val())
        else:
            raise NonCriticalError("Not integerConstant")

    def compile_string_term(self) -> None:
        """tries to compile a term that is a stringConstant"""
        char_set = {
            " ": 32, "!": 33, '"': 34, "#": 35, "$": 36, "%": 37,
            "&": 38, "'": 39, "(": 40, ")": 41, "*": 42, "+": 43,
            ",": 44, "-": 45, ".": 46, "/": 47, "0": 48, "1": 49,
            "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55,
            "8": 56, "9": 57, ":": 58, ";": 59, "<": 60, "=": 61,
            ">": 62, "?": 63, "@": 64, "A": 65, "B": 66, "C": 67,
            "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73,
            "J": 74, "K": 75, "L": 76, "M": 77, "N": 78, "O": 79,
            "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84, "U": 85,
            "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "[": 91,
            "\\": 92, "]": 93, "^": 94, "_": 95, "’": 96, "a": 97,
            "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103,
            "h": 104, "i": 105, "j": 106, "k": 107, "l": 108, "m": 109,
            "n": 110, "o": 111, "p": 112, "q": 113, "r": 114, "s": 115,
            "t": 116, "u": 117, "v": 118, "w": 119, "x": 120, "y": 121,
            "z": 122, "{": 123, "": 124, "}": 125, "~": 126  # TODO the rest
        }
        # check if token is STRING_CONST
        if self.tokenizer.token_type() == "STRING_CONST":
            # write stringConstant to file
            str_const = self.tokenizer.string_val()
            self.out_stream.write(f"<stringConstant> {str_const} </stringConstant>\n")
            # call string constructor, save value in temp 1
            self.writer.write_call("String.new", 0)
            self.writer.write_pop("temp", 1)
            # for each character, push the corresponding value according
            # to the Jack Character Set, calling appendChar for each char
            for char in str_const:
                self.writer.write_push("temp", 1)
                self.writer.write_push("constant", char_set[char])
                self.writer.write_call("appendChar", 0)

        else:
            raise NonCriticalError("Not stringConstant")

    def compile_keyword_term(self) -> None:
        """Tries to compile a term that is a keywordConstant"""
        # try to write keyword token
        # from the subset ["THIS", "NULL", "TRUE", "FALSE"]
        keyword_constants = ["THIS", "NULL", "TRUE", "FALSE"]
        try:
            self.__write_keyword(keyword_constants)
            self.writer.write_push(self.tokenizer.keyword(), 0)
        except KeywordError:
            raise NonCriticalError("Not KeywordConstant")

    def compile_array_addressing(self) -> None:
        """Tries to compile a term that is an addressing to an array"""
        # check if look ahead token is [
        peak = self.tokenizer.get_look_ahead_token()
        if peak == "[":
            # write varName
            try:
                # align that to (arr + i)
                # push address of array
                self.__write_var_name(push=True)
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
                # assume result of expression (i) at top of stack
                # add
                self.writer.write_arithmetic("+")
                # pop to pointer 1
                self.writer.write_pop("pointer", 1)
                self.__write_symbol("]")
                self.writer.write_push("that", 0)
            except IdentifierError as identifier:
                raise CriticalError(identifier.message())
            except SymbolError as symbol:
                raise CriticalError(symbol)
            except CriticalError as critical:
                raise critical
        else:
            raise NonCriticalError("Not array addressing")

    def __write_generic_subroutine(self) -> int:
        """writes the generic subroutine call"""
        n_args: int = 0
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
            n_args = self.compile_expression_list()
            # write )
            self.__write_symbol(")")
            return n_args
        except IdentifierError as identifier:
            raise CriticalError(identifier.message())
        except SymbolError as symbol:
            raise CriticalError(symbol)
        except CriticalError as critical:
            raise critical
        except NonCriticalError:
            pass

    def __object_method_call(self) -> None:
        ident = self.tokenizer.identifier()
        # check if ident in cur scope or outer scope
        if self.sym_table.search_in_cur_scope(ident):
            # push the address of the object onto the stack as argument 0
            self.writer.write_push(self.sym_table.kind_of(ident), self.sym_table.index_of(ident))
        elif self.sym_table.search_in_out_outer(ident):
            self.writer.write_push(self.sym_table.outer_kind_of(ident), self.sym_table.outer_index_of(ident))

    def compile_subroutine_term(self, related=False) -> int:
        """Tries to compile a term that is a call to a subroutine"""
        func_name = self.__get_function_name()
        # if look ahead token is (, compile subroutineCall
        peak = self.tokenizer.get_look_ahead_token()
        n_args: int = 0
        try:
            if peak == "(":
                n_args = self.__write_generic_subroutine()

            # if look-ahead token is ., subroutine call will come from class name
            elif peak == ".":
                try:
                    self.__write_var_name()
                    # check if identifier in symbol table, if true
                    # push the base address of the object onto
                    self.__object_method_call()
                except IdentifierError:
                    self.__write_class_name_keyword()
                    self.__object_method_call()
                self.__check_tokenizer()
                self.tokenizer.advance()
                self.__write_symbol(".")
                self.__check_tokenizer()
                self.tokenizer.advance()
                n_args = self.compile_subroutine_term(True)
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
        if not related:
            self.writer.write_call(func_name, n_args)
        return n_args

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
            unary_op = self.tokenizer.symbol()
            self.__check_tokenizer()
            self.tokenizer.advance()
            # write term
            self.out_stream.write("<term>\n")
            self.compile_term()
            self.out_stream.write("</term>\n")
            # write unary operator to vm
            if unary_op == "-":
                unary_op = "!"
            self.writer.write_arithmetic(unary_op)
        except CriticalError as critical:
            raise critical
        except SymbolError:
            raise NonCriticalError("Not unary op")

    def compile_expression_list(self, new=True) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        # set counter for n_args
        n_args: int = 0
        # try to compile expression
        if new:
            self.out_stream.write("<expressionList>\n")
        try:
            if not self.__check_closer(")"):
                self.compile_expression()
                self.__check_tokenizer()
                self.tokenizer.advance()
                n_args += 1
            else:
                n_args = 0
            # try to write comma symbol
            self.__write_symbol(",")
            self.__check_tokenizer()
            self.tokenizer.advance()
            # call compile_expression_list
            n_args += self.compile_expression_list(False)
        except CriticalError as critical:
            raise critical
        except SymbolError as symbol:
            raise CriticalError(symbol.message())
        except NonCriticalError:
            return n_args
        # finally, could be empty, return
        finally:
            if new:
                self.out_stream.write("</expressionList>\n")
            return n_args

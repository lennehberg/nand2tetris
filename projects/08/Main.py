"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_push_pop(parser: Parser, code_writer: CodeWriter) -> None:
    cur_type = parser.command_type()
    segment = parser.arg1()
    index = parser.arg2()
    code_writer.write_push_pop(cur_type, segment, index)


def translate_arithmetic(parser: Parser, code_writer: CodeWriter) -> None:
    cur_cmmnd = parser.arg1()
    code_writer.write_arithmetic(cur_cmmnd)


def translate_label(parser: Parser, code_writer: CodeWriter) -> None:
    cur_label = parser.arg1()
    code_writer.write_label(cur_label)


def translate_goto(parser: Parser, code_writer: CodeWriter) -> None:
    cur_label = parser.arg1()
    code_writer.write_goto(cur_label)


def translate_if(parser: Parser, code_writer: CodeWriter) -> None:
    cur_label = parser.arg1()
    code_writer.write_if(cur_label)


def translate_function(parser: Parser, code_writer: CodeWriter) -> None:
    function_name = parser.arg1()
    n_vars = parser.arg2()
    code_writer.write_function(function_name, n_vars)


def translate_call(parser: Parser, code_writer: CodeWriter):
    function = parser.arg1()
    n_vars = parser.arg2()
    code_writer.write_call(function, n_vars)


def translate_return(code_writer: CodeWriter):
    code_writer.write_return()


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # It might be good to start with something like:
    # parser = Parser(input_file)
    # code_writer = CodeWriter(output_file)
    # init parser and code_writer
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    code_writer.set_file_name("Sys")
    code_writer.write_init()

    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    code_writer.set_file_name(input_filename)

    while parser.has_more_commands():
        cur_type = parser.command_type()
        # command is of type "C_PUSH" or "C_POP"
        if cur_type == "C_PUSH" or cur_type == "C_POP":
            translate_push_pop(parser, code_writer)
        # command is a "C_ARITHMETIC"
        elif cur_type == "C_ARITHMETIC":
            translate_arithmetic(parser, code_writer)
        elif cur_type == "C_LABEL":
            # translate label command
            translate_label(parser, code_writer)
        elif cur_type == "C_GOTO":
            # translate goto command
            translate_goto(parser, code_writer)
        elif cur_type == "C_IF":
            # translate if command
            translate_if(parser, code_writer)
        elif cur_type == "C_FUNCTION":
            # translate function command
            translate_function(parser, code_writer)
        elif cur_type == "C_CALL":
            # translate call command
            translate_call(parser, code_writer)
        elif cur_type == "C_RETURN":
            translate_return(code_writer)

        parser.advance()
    pass


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)

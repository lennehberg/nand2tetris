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
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")

    # objects init
    parser = Parser(input_file)
    sym_table = SymbolTable()

    # first pass
    if not first_pass(parser, sym_table):
        print("SYMBOL ERROR!")
        return
    parser.reset()
    # second pass
    second_pass(parser, sym_table)
    parser.reset()
    # translate
    translate(output_file, parser, sym_table)
    pass


def translate(output_file: typing.TextIO, parser: Parser, sym_table: SymbolTable):
    full_addr: str = ""
    while parser.has_more_commands():
        if parser.command_type() == "A_COMMAND":
            sym = parser.symbol()
            if not sym.isdigit():
                addr = bin(sym_table.get_address(sym))
                addr = addr[2:]
            else:
                addr = bin(int(sym))
                addr = addr[2:]  # remove the 0b prefix from binary string
            if len(addr) < 16:
                full_addr = ((16 - len(addr)) * "0") + addr
            else:
                full_addr = addr  # assuming length of address cant be longer than 16 bits
        elif parser.command_type() == "C_COMMAND":
            full_addr = "111" + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump())  # "111" + "acccccc" + "ddd" + "jjj"
        elif parser.command_type() == "C_COMMAND_SHIFT":
            full_addr = "101" + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump())
        if not parser.command_type() == "L_COMMAND":
            output_file.write(full_addr + "\n")
        full_addr = ""

        parser.advance()
    pass


def first_pass(parser: Parser, sym_table: SymbolTable) -> bool:
    # init an address counter
    counter: int = 0
    # parse all the LABEL pseduo-commands, putting them in symbol table 
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            sym = parser.symbol()
            if not (valid_symbol(sym)):
                return False
            else:
                if not (sym_table.contains(sym)):
                    sym_table.add_entry(sym, counter)
        else:
            counter += 1
        parser.advance()
    return True
    pass


def second_pass(parser: Parser, sym_table: SymbolTable):
    # init a counter for proper placements
    counter: int = 16
    while parser.has_more_commands():
        if parser.command_type() == "A_COMMAND":
            sym = parser.symbol()
            if not sym.isdigit():
                if not sym_table.contains(sym):
                    sym_table.add_entry(sym, counter)
                    counter += 1
        parser.advance()
    pass


def valid_symbol(symbol: str) -> bool:
    if '0' < symbol[0] < '9':
        return False

    legal_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                  "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                  "_", ".", ":", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "$"]

    for char in symbol:
        if char not in legal_char:
            return False
    return True
    pass


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)

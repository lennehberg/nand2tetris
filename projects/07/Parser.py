"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        # set self.commands to be a formatted text,
        # no whitespaces, no comments
        self.commands = input_file.read().strip().splitlines()
        self.count = 0
        self.total = len(self.commands)
        self.remove_comments()
        self.cur = self.commands[0]
        pass

    def remove_comments(self) -> None:
        """Removes comments and whitespaces from commands
        """
        i: int = 0
        while i < self.total:
            # self.commands[i] = self.commands[i].replace(" ", "")
            if self.commands[i].startswith("//") or self.commands[i] == "":
                self.commands.remove(self.commands[i])
                i -= 1
                self.total = self.total - 1
            else:
                for j in range(len(self.commands[i])):
                    if self.commands[i][j] == "/":
                        self.commands[i] = self.commands[i][:j]
                        break
            i += 1

    pass

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.count >= self.total:
            return False
        return True
        pass

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.count += 1
        if self.count < self.total:
            self.cur = self.commands[self.count]
        pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        temp = self.cur.split()
        arithmetics = {"add", "sub", "neg", "and", "or", "not", "shifleft", "shiftright", "eq", "gt", "lt"}
        cmd: str = ""
        if temp[0] == "push":
            cmd = "C_PUSH"
        elif temp[0] == "pop":
            cmd = "C_POP"
        elif temp[0] in arithmetics:
            cmd = "C_ARITHMETIC"
        """TODO project 8 stuff"""

        return cmd

        pass

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        temp = self.cur.split()
        if self.command_type() == "C_ARITHMETIC":
            return temp[0]
        return temp[1]
        pass

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        temp = self.cur.split()
        return int(temp[2])
        pass

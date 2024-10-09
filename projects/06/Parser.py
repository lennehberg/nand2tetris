"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


# HELPER TO REMOVE COMMENTS
def remove_comments(commands) -> None:
    length = len(commands)
    i: int = 0
    while i < length:
        commands[i] = commands[i].replace(" ", "")
        if commands[i].startswith("//") or commands[i] == "":
            commands.remove(commands[i])
            i -= 1
            length = length - 1
        else:
            for j in range(len(commands[i])):
                if commands[i][j] == "/":
                    commands[i] = commands[i][:j]
                    break
        i += 1
    pass


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.commands = input_file.read().strip().splitlines()
        remove_comments(self.commands)
        self.cur = self.commands[0]
        self.count = 0
        self.total = len(self.commands)

    def reset(self):
        self.cur = self.commands[0]
        self.count = 0
        pass

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.count >= self.total:
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.count += 1
        while (self.has_more_commands()
               and
               (self.commands[self.count].isspace() or self.commands[self.count].startswith("//"))):
            self.count += 1
        if not self.count >= self.total:
            self.cur = self.commands[self.count]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        is_l: bool = False
        is_a: bool = False
        is_shift: bool = False

        for i in range(len(self.cur)):
            if self.cur[i] == "(":
                is_l = True
            if self.cur[i] == "@":
                is_a = True
            if i < len(self.cur) - 1:
                if ((self.cur[i] == ">" and self.cur[i + 1] == ">") or
                        (self.cur[i] == "<" and self.cur[i + 1] == "<")):
                    is_shift = True

        if is_a:
            command_type = "A_COMMAND"
        elif is_l:
            command_type = "L_COMMAND"
        else:
            if is_shift:
                command_type = "C_COMMAND_SHIFT"
            else:
                command_type = "C_COMMAND"

        return command_type

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        sym = self.cur
        sym = sym.replace('@', '').replace('(', '').replace(')', '')
        return sym
        pass

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        com = self.cur.strip()
        com = com.split("=")
        dest = com[0]
        return dest

        pass

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """

        # iterate over cur and check if = or ; are present
        has_equal: bool = False
        has_semi: bool = False
        com: str = ""
        counter: int = 0
        e_ind: int = 0
        s_ind: int = len(self.cur)
        for char in self.cur:
            if char == "=":
                has_equal = True
                e_ind = counter
            if char == ";":
                has_semi = True
                s_ind = counter
            counter += 1

        if has_equal and has_semi:
            com = self.cur[e_ind + 1:s_ind]
        elif has_equal:
            com = self.cur[e_ind + 1:]
        elif has_semi:
            com = self.cur[:has_semi]
        return com
        pass

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        com = self.cur.split(";")
        if len(com) == 1:
            return "null"
        else:
            jump = com[1]
        return jump

        pass

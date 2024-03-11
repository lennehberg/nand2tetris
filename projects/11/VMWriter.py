"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.out_stream = output_stream
        pass

    @staticmethod
    def __get_segment(segment) -> str:
        segments = ["CONST", "ARG", "LOCAL", "STATIC",
                    "THIS", "THAT", "POINTER", "TEMP"]
        segments_vm = ["constant", "argument", "local", "static",
                       "this", "that", "pointer", "temp"]
        for i in range(len(segments)):
            if segment == segments[i]:
                segment = segments_vm[i]
        return segment

    @staticmethod
    def __get_arithmetic(op) -> str:
        """arithmetic(str): the command to return, can be "ADD", "SUB", "NEG",
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT"."""
        op_jack = ["+", "-", "~", "=", ">", "<", "&", "|", "^", "#", "!"]
        math_op = ["*", "/"]
        math_funcs = ["Math.multiply", "Math.divide"]
        op_vm = ["add", "sub", "not", "eq", "gt", "lt", "and", "or", "shiftleft", "shiftright", "neg"]
        for i in range(len(op_jack)):
            if op == op_jack[i]:
                return op_vm[i]

        for i in range(len(math_op)):
            if op == math_op[i]:
                return math_funcs[i]

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        if segment == "TRUE":
            self.out_stream.write("push constant 1\n")
            self.out_stream.write("neg\n")
        elif segment == "FALSE" or segment == "NULL":
            self.out_stream.write("push constant 0\n")
        elif segment == "FIELD":
            self.out_stream.write(f"push this {index}\n")
        else:
            segment = self.__get_segment(segment)
            self.out_stream.write(f"push {segment} {index}\n")

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        if segment == "TRUE":
            self.out_stream.write("pop constant 1\n")
            self.out_stream.write("neg\n")
        elif segment == "FALSE" or segment == "NULL":
            self.out_stream.write("pop constant 0\n")
        elif segment == "FIELD":
            self.out_stream.write(f"pop this {index}\n")
        else:
            segment = self.__get_segment(segment)
            self.out_stream.write(f"pop {segment} {index}\n")

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        math_funcs = ["Math.multiply", "Math.divide"]
        command = self.__get_arithmetic(command)
        if command in math_funcs:
            self.write_call(command, 2)
        else:
            self.out_stream.write(f"{command}\n")

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        self.out_stream.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        self.out_stream.write(f"goto {label}\n")

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.out_stream.write(f"if-goto {label}\n")
        pass

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        self.out_stream.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        self.out_stream.write(f"function {name} {n_locals}\n")

    def write_return(self, has_statements) -> None:
        """Writes a VM return command."""
        if not has_statements:
            self.write_push("constant", 0)
        self.out_stream.write(f"return\n")

    def write_comment(self, msg: str) -> None:
        """writes message as a comment in vm"""
        self.out_stream.write(f"// {msg}\n")

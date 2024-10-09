"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

"""
DECORATORS
"""


def sys_counter(func):
    counter = 0

    def wrapper(*args, **kwargs):
        nonlocal counter
        counter += 1
        if counter > 1:
            return None
        else:
            return func(*args, **kwargs)

    return wrapper


def call_counter(func):
    counter = 0

    def wrapper(*args, **kwargs):
        nonlocal counter
        counter += 1
        mod_args = list(args)
        mod_args.append(counter)
        return func(*mod_args, **kwargs)

    return wrapper


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.filename: str = ""
        self.out_stream: typing.TextIO = output_stream
        self.cond_count: int = 0
        self._segments = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        self.cur_func: str = ""
        self.has_init = False

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    """Writes assembly code that initializes the VM"""

    @sys_counter
    def write_init(self) -> None:
        if not self.has_init:
            asm_init = "@256\n"
            asm_init += "D=A\n"
            asm_init += "@SP\n"
            asm_init += "M=D\n"
            self.out_stream.write(asm_init)
            self.write_call("Sys.init", 0)

        self.has_init = True

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        # add comment to file
        self.out_stream.write("// " + command + "\n")
        # check what to do
        binary = {
            "add": "+",
            "sub": "-",
            "and": "&",
            "or": "|"
        }

        unary = {
            "neg": "-",
            "not": "!",
            "shiftleft": "<<",
            "shiftright": ">>"
        }

        conditionals = ["lt", "gt", "eq"]
        # if binary operator
        asm_str: str = ""
        if command in binary:
            # go to head of stack, add value to D

            # @SP
            # A=M-1
            # D=M
            asm_str = "@SP\n"
            asm_str += "A=M-1\n"
            asm_str += "D=M\n"

            # go to next item in stack,
            # perform operator on M
            # and put in M

            # A=A-1
            # D=M<OP>D
            asm_str += "A=A-1\n"
            asm_str += "M=M" + binary.get(command) + "D\n"

            # update stack pointer

            # @SP
            # M=M-1
            asm_str += self.__update_sp("C_POP")

        elif command in unary:
            # if unary operator
            # go to head of stack

            # @SP
            # A=A-1
            asm_str += "@SP\n"
            asm_str += "A=M-1\n"

            # manipulate value according to op
            if command == "neg" or command == "not":
                asm_str += "M=" + unary.get(command) + "M\n"
                # M=<OP>M
            else:
                # shift M value
                asm_str += "M=M" + unary.get(command) + "\n"

        # if command is gt/lt/eq
        elif command in conditionals:
            # subtract between 2 first elements
            asm_str += "@SP\n"
            asm_str += "A=M-1\n"
            asm_str += "D=M\n"
            asm_str += "A=A-1\n"
            asm_str += "D=M-D\n"

            # if value is 0, then JUMP to (SET_SP_TRUE) if command is eq
            if command == "eq":
                # JUMP if JEQ
                asm_str += "@SET_SP_TRUE." + str(self.cond_count) + "\n"
                asm_str += "D;JEQ\n"

            # if value is <0, then JUMP to (SET_SP_TRUE) if command is lt
            elif command == "lt":
                # JUMP if JLT
                asm_str += "@SET_SP_TRUE." + str(self.cond_count) + "\n"
                asm_str += "D;JLT\n"

            # if value is >0, then JUMP to (SET_SP_TRUE) if command is gt
            elif command == "gt":
                # JUMP if JGT
                asm_str += "@SET_SP_TRUE." + str(self.cond_count) + "\n"
                asm_str += "D;JGT\n"

            # else JUMP to (SET_SP_FALSE)
            asm_str += "@SET_SP_FALSE." + str(self.cond_count) + "\n"
            asm_str += "0;JMP\n"

            # set up (SET_SP_TRUE)
            asm_str += "(SET_SP_TRUE." + str(self.cond_count) + ")\n"
            asm_str += self.__update_sp("C_POP")
            asm_str += "M=M-1\n"
            # set D to true (-1)
            asm_str += "D=-1\n"
            # push D onto SP
            asm_str += self.__push_val()
            # update SP
            asm_str += self.__update_sp("C_PUSH")
            # JUMP to (END_SP_SET_BOOL)
            asm_str += "@END_SP_SET_BOOL." + str(self.cond_count) + "\n"
            asm_str += "0;JMP\n"

            # set up (SET_SP_FALSE)
            asm_str += "(SET_SP_FALSE." + str(self.cond_count) + ")\n"
            asm_str += self.__update_sp("C_POP")
            asm_str += "M=M-1\n"
            # set D to be false (0)
            asm_str += "D=0\n"
            # push D onto SP
            asm_str += self.__push_val()
            # update sp
            asm_str += self.__update_sp("C_PUSH")
            # set up (END_SP_SET_BOOL)
            asm_str += "(END_SP_SET_BOOL." + str(self.cond_count) + ")\n"

            self.cond_count += 1
        self.out_stream.write(asm_str)

    def __get_address(self, segment: str, index: int) -> str:
        asm: str = ""
        # if segment is local/argument/this/that/temp
        if segment in self._segments:
            # save index in D
            asm += "@" + str(index) + "\n"
            # go to base address of segment
            asm += "D=A\n"
            # go to segment at index (LCL + 3 i.e)
            asm += "@" + self._segments.get(segment) + "\n"
            asm += "A=M+D\n"
            # asm += "D=M\n"

        elif segment == "temp":
            asm += "@" + str(index) + "\n"
            asm += "D=A\n"
            asm += "@5\n"
            asm += "A=A+D\n"

        # if segment is constant
        elif segment == "constant":
            # go to address of constant
            if index > 32767:
                raise Exception("MEMORY ADDRESS OVERFLOW!")

            asm += "@" + str(index) + "\n"
            # save A value to D
            # asm += "D=A\n"

            # if segment is static
        elif segment == "static":
            # go to @<FUNCTION_NAME>.<index>
            asm += "@" + self.filename + "." + str(index) + "\n"
            # set D to M value
            # asm += "D=M\n"

        # if segment is pointer
        elif segment == "pointer":
            # if pointer 0 then save THIS to D
            if index == 0:
                asm += "@THIS\n"
                # asm += "D=M\n"
            # if pointer 1 then save THAT to D
            elif index == 1:
                asm += "@THAT\n"
                # asm += "D=M\n"
        return asm

    """Pushes val from D to head of stack"""

    @staticmethod
    def __push_val() -> str:
        asm: str = ""
        # go to head of stack
        asm += "@SP\n"
        asm += "A=M\n"
        # save value to head of stack
        asm += "M=D\n"
        return asm

    """pops val to D from head of stack"""

    @staticmethod
    def __pop_val() -> str:
        asm: str = ""
        asm += "@SP\n"
        asm += "A=M-1\n"
        asm += "D=M\n"
        return asm

    """updates sp shifts amount of times, default 1"""

    @staticmethod
    def __update_sp(command: str, shifts: int = 1) -> str:
        asm: str = ""
        # update stack pointer if push
        if command == "C_PUSH":
            asm += "@" + str(shifts) + "\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=M+D\n"
        # if pop
        elif command == "C_POP":
            asm += "@R14\n"
            asm += "M=D\n"
            asm += "@" + str(shifts) + "\n"
            asm += "D=A\n"
            asm += "@SP\n"
            asm += "M=M-D\n"
            asm += "@R14\n"
            asm += "D=M\n"
        return asm

    def __do_push(self, segment: str, index: int) -> str:
        asm: str = ""
        # get address of variable
        asm += self.__get_address(segment, index)
        # get value from address
        if segment == "constant":
            asm += "D=A\n"
        else:
            asm += "D=M\n"
        # push into head of stack
        asm += self.__push_val()
        # update SP
        asm += self.__update_sp("C_PUSH")
        return asm

    def __do_pop(self, segment: str, index: int) -> str:
        asm: str = ""
        # save address to RAM[13]
        asm += self.__get_address(segment, index)
        asm += "D=A\n"
        asm += "@R13\n"
        asm += "M=D\n"

        # pop value from head of stack
        asm += self.__pop_val()
        # update sp
        asm += self.__update_sp("C_POP")
        # go to address
        asm += "@R13\n"
        asm += "A=M\n"
        # put value in slot
        asm += "M=D\n"
        return asm

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        asm_str: str = ""

        # print command
        com = "push " if command == "C_PUSH" else "pop "
        self.out_stream.write("// " + com + " " + segment + " " + str(index) + "\n")
        # check if push or pop
        if command == "C_PUSH":
            # do push
            asm_str += self.__do_push(segment, index)
        elif command == "C_POP":
            # do pop
            asm_str += self.__do_pop(segment, index)
        self.out_stream.write(asm_str)

    def generate_label_name(self, label: str) -> str:
        return self.cur_func + "$" + label

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # write comment
        com = "// label " + label + "\n"
        self.out_stream.write(com)
        # get label declaration like mentions above
        asm_label = "(" + self.generate_label_name(label) + ")\n"
        # write label to file
        self.out_stream.write(asm_label)
        pass

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # write command
        com = "// goto " + label + "\n"
        self.out_stream.write(com)
        # generate label
        asm_goto = "@" + self.generate_label_name(label) + "\n"
        # unconditional jump to label
        asm_goto += "0;JMP\n"
        # write to file
        self.out_stream.write(asm_goto)
        pass

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # write comment
        com = "// if-goto " + label + "\n"
        self.out_stream.write(com)
        # check stack head true or false
        asm_if_goto = "// check stack head true of false\n"
        asm_if_goto += "@SP\n"
        asm_if_goto += "A=M-1\n"
        asm_if_goto += "D=M\n"
        # generate label
        asm_if_goto += "@" + self.generate_label_name(label) + "\n"
        # if NEQ (meaning the result value residing in stack is true), jump to label
        asm_if_goto += "D;JNE\n"
        # write to file
        self.out_stream.write(asm_if_goto)
        pass

    """pushes 0 n amount of times in assembly
    Args:
        n (int) amount of pushes
    """

    @call_counter
    def __write_looped_push(self, n: int, count=0) -> None:
        loop_push_asm = "// push 0 n_vars\n"
        loop_push_asm += "@" + str(n-1) + "\n"
        loop_push_asm += "D=A\n"
        loop_push_asm += "(LOOPED_PUSH." + str(count) + ")\n"
        loop_push_asm += "@SP\n"
        loop_push_asm += "A=M+D\n"
        loop_push_asm += "M=0\n"
        loop_push_asm += "A=A+1\n"
        loop_push_asm += "D=D-1\n"
        loop_push_asm += "@CONT." + str(count) + "\n"
        loop_push_asm += "D;JLT\n"
        loop_push_asm += "@LOOPED_PUSH." + str(count) + "\n"
        loop_push_asm += "0;JMP\n"
        loop_push_asm += "(CONT." + str(count) + ")\n"
        self.cond_count += 1

        loop_push_asm += self.__update_sp("C_PUSH", n)
        self.out_stream.write(loop_push_asm)

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.cur_func = function_name
        com = "// function " + function_name + "\n"
        self.out_stream.write(com)
        asm_func = "(" + function_name + ")\n"
        self.out_stream.write(asm_func)
        if not n_vars == 0:
            self.__write_looped_push(n_vars)

    @staticmethod
    @call_counter
    def generate_return_name(function_name, call_count) -> str:
        # get label declaration like mentions above
        asm_label = function_name + "." + str(call_count)
        # write label to file
        return asm_label

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        com = "// call " + function_name + "\n"
        self.out_stream.write(com)
        # save n_vars to RAM[14]
        asm_call = "// save n_vars to RAM[14]\n"
        """TODO make sure calling sys.init is the same stack wise"""
        asm_call += "@" + str(n_args) + "\n"
        asm_call += "D=A\n"
        asm_call += "@R14\n"
        asm_call += "M=D\n"
        # save current address of head of stack to RAM[15], for ARG repositioning
        asm_call += "// save current address of head of stack to RAM[15], for ARG repositioning\n"

        asm_call += "@SP\n"
        asm_call += "D=M\n"
        asm_call += "@R15\n"
        asm_call += "M=D\n"
        # generate a return name for label and return address
        ret_name = self.generate_return_name(function_name)
        # push return address
        asm_call += "// push return address\n"

        asm_call += "@" + ret_name + "\n"
        asm_call += "D=A\n"
        asm_call += self.__push_val()
        asm_call += self.__update_sp("C_PUSH")
        # push LCL
        asm_call += "// push LCL\n"

        asm_call += "@LCL\n"
        asm_call += "D=M\n"
        asm_call += self.__push_val()
        asm_call += self.__update_sp("C_PUSH")
        # push ARG
        asm_call += "// push ARG\n"

        asm_call += "@ARG\n"
        asm_call += "D=M\n"
        asm_call += self.__push_val()
        asm_call += self.__update_sp("C_PUSH")
        # push THIS
        asm_call += "// push THIS\n"

        asm_call += "@THIS\n"
        asm_call += "D=M\n"
        asm_call += self.__push_val()
        asm_call += self.__update_sp("C_PUSH")
        # push THAT
        asm_call += "// push THAT\n"

        asm_call += "@THAT\n"
        asm_call += "D=M\n"
        asm_call += self.__push_val()
        asm_call += self.__update_sp("C_PUSH")
        # reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])
        asm_call += "// reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])\n"
        asm_call += "@SP\n"
        asm_call += "D=M\n"
        asm_call += "@5\n"
        asm_call += "D=D-A\n"
        asm_call += "@" + str(n_args) + "\n"
        asm_call += "D=D-A\n"
        asm_call += "@ARG\n"
        asm_call += "M=D\n"

        # reposition LCL = SP
        asm_call += "// reposition LCL = SP\n"
        asm_call += "@SP\n"
        asm_call += "D=M\n"
        asm_call += "@LCL\n"
        asm_call += "M=D\n"
        # goto function name
        asm_call += "// goto function name\n"

        asm_call += "@" + function_name + "\n"
        asm_call += "0;JMP\n"
        # return label
        asm_call += "// return label\n"

        asm_call += "(" + ret_name + ")\n"
        self.out_stream.write(asm_call)

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        com = "// return\n"
        self.out_stream.write(com)
        # save LCL to RAM[15]
        ret_asm = "// Save LCL to RAM[15]\n"
        ret_asm += "@LCL\n"
        ret_asm += "D=M\n"
        ret_asm += "@R15\n"
        ret_asm += "M=D\n"

        # save return address to return_addr
        ret_asm += "@5\n"
        ret_asm += "D=A\n"
        ret_asm += "@R15\n"
        ret_asm += "A=M-D\n"
        ret_asm += "D=M\n"
        ret_asm += "@RET_AD\n"
        ret_asm += "M=D\n"

        # reposition the return value for the caller
        ret_asm += "// Reposition the return value for the caller\n"
        ret_asm += self.__pop_val()
        ret_asm += "@ARG\n"
        ret_asm += "A=M\n"
        ret_asm += "M=D\n"
        ret_asm += self.__update_sp("C_POP")
        # reposition SP
        ret_asm += "// Reposition SP\n"
        ret_asm += "@ARG\n"
        ret_asm += "D=M+1\n"
        ret_asm += "@SP\n"
        ret_asm += "M=D\n"
        # restores THAT to caller
        ret_asm += "// Restores THAT to caller\n"
        ret_asm += "@R15\n"
        ret_asm += "A=M-1\n"
        ret_asm += "D=M\n"
        ret_asm += "@THAT\n"
        ret_asm += "M=D\n"
        # restores THIS to caller
        ret_asm += "// Restores THIS to caller\n"
        ret_asm += "@2\n"
        ret_asm += "D=A\n"
        ret_asm += "@R15\n"
        ret_asm += "A=M-D\n"
        ret_asm += "D=M\n"
        ret_asm += "@THIS\n"
        ret_asm += "M=D\n"
        # restores ARG to caller
        ret_asm += "// Restores ARG to the caller\n"
        ret_asm += "@3\n"
        ret_asm += "D=A\n"
        ret_asm += "@R15\n"
        ret_asm += "A=M-D\n"
        ret_asm += "D=M\n"
        ret_asm += "@ARG\n"
        ret_asm += "M=D\n"
        # restores LCL to caller
        ret_asm += "// Restores LCL to caller\n"
        ret_asm += "@4\n"
        ret_asm += "D=A\n"
        ret_asm += "@R15\n"
        ret_asm += "A=M-D\n"
        ret_asm += "D=M\n"
        ret_asm += "@LCL\n"
        ret_asm += "M=D\n"
        # goto return address (stored in return_addr)
        ret_asm += "// goto return address\n"
        ret_asm += "@RET_AD\n"
        ret_asm += "A=M\n"
        ret_asm += "0;JMP\n"
        self.out_stream.write(ret_asm)

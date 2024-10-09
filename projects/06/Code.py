"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        dest_bin: str = "000"
        if mnemonic == "M":
            dest_bin = "001"
        elif mnemonic == "D":
            dest_bin = "010"
        elif mnemonic == "MD":
            dest_bin = "011"
        elif mnemonic == "A":
            dest_bin = "100"
        elif mnemonic == "AM":
            dest_bin = "101"
        elif mnemonic == "AD":
            dest_bin = "110"
        elif mnemonic == "AMD":
            dest_bin = "111"
        return dest_bin
        pass

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        comp_bin = "0000000"

        if mnemonic == "0":
            comp_bin = "0101010"
        elif mnemonic == "1":
            comp_bin = "0111111"
        elif mnemonic == "-1":
            comp_bin = "0111010"
        elif mnemonic == "D":
            comp_bin = "0001100"
        elif mnemonic == "A":
            comp_bin = "0110000"
        elif mnemonic == "M":
            comp_bin = "1110000"
        elif mnemonic == "!D":
            comp_bin = "0001101"
        elif mnemonic == "!A":
            comp_bin = "0110001"
        elif mnemonic == "!M":
            comp_bin = "1110001"
        elif mnemonic == "!D":
            comp_bin = "0110001"
        elif mnemonic == "-D":
            comp_bin = "0001111"
        elif mnemonic == "-A":
            comp_bin = "0110011"
        elif mnemonic == "-M":
            comp_bin = "1110011"
        elif mnemonic == "D+1" or mnemonic == "1+D":
            comp_bin = "0011111"
        elif mnemonic == "A+1" or mnemonic == "1+A":
            comp_bin = "0110111"
        elif mnemonic == "M+1" or mnemonic == "1+M":
            comp_bin = "1110111"
        elif mnemonic == "D-1":
            comp_bin = "0001110"
        elif mnemonic == "A-1":
            comp_bin = "0110010"
        elif mnemonic == "M-1":
            comp_bin = "1110010"
        elif mnemonic == "D+A" or mnemonic == "A+D":
            comp_bin = "0000010"
        elif mnemonic == "D+M" or mnemonic == "M+D":
            comp_bin = "1000010"
        elif mnemonic == "D-A":
            comp_bin = "0010011"
        elif mnemonic == "D-M":
            comp_bin = "1010011"
        elif mnemonic == "A-D":
            comp_bin = "0000111"
        elif mnemonic == "M-D":
            comp_bin = "1000111"
        elif mnemonic == "D&A" or mnemonic == "A&D":
            comp_bin = "0000000"
        elif mnemonic == "D&M" or mnemonic == "M&D":
            comp_bin = "1000000"
        elif mnemonic == "D|A" or mnemonic == "A|D":
            comp_bin = "0010101"
        elif mnemonic == "D|M" or mnemonic == "M|D":
            comp_bin = "1010101"
        elif mnemonic == "A<<":
            comp_bin = "0100000"
        elif mnemonic == "D<<":
            comp_bin = "0110000"
        elif mnemonic == "M<<":
            comp_bin = "1100000"
        elif mnemonic == "A>>":
            comp_bin = "0000000"
        elif mnemonic == "D>>":
            comp_bin = "0010000"
        elif mnemonic == "M>>":
            comp_bin = "1000000"
        return comp_bin
        pass

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        jump_bin = "000"

        if not mnemonic:
            jump_bin = "000"
        if mnemonic == "JGT":
            jump_bin = "001"
        if mnemonic == "JEQ":
            jump_bin = "010"
        if mnemonic == "JGE":
            jump_bin = "011"
        if mnemonic == "JLT":
            jump_bin = "100"
        if mnemonic == "JNE":
            jump_bin = "101"
        if mnemonic == "JLE":
            jump_bin = "110"
        if mnemonic == "JMP":
            jump_bin = "111"
        return jump_bin
        pass

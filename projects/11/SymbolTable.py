"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

# declaring global variables for ease of use
NAME = 0
TYPE = 1
KIND = 2
INDEX = 3

N_LOCALS = 1
N_ARGS = 2

LCL = 0
ARG = 1
STATIC = 2
FIELD = 3


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # creates a list containing 3 lists, symbolising our table, where:
        # 0 - TYPE, 1 - KIND, 2 - INDEX
        self.var_table = []
        self.func_table = []
        self.type_count_arr = [0 for _ in range(4)]  # declare a type counter for counting types
        self.subroutine_table = None  # declare a variable for subroutine's table, allowing scoping
        self.cur = self  # declare a cur to know which scope we're manipulating

    @staticmethod
    def __get_kind(kind: str) -> int:
        if kind == "STATIC":
            return STATIC
        if kind == "FIELD":
            return FIELD
        if kind == "LOCAL":
            return LCL
        if kind == "ARG":
            return ARG
        else:
            return -1

    def __search_for_name(self, name: str, table: str) -> list:
        """searches for name in table"""
        if table == "var":
            for item in self.cur.var_table:
                if name == item[NAME]:
                    return item
        return []

    def __search_for_outer_name(self, name: str, table: str) -> list:
        """searches for name in table"""
        if table == "var":
            for item in self.var_table:
                if name == item[NAME]:
                    return item
        return []

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_table = SymbolTable()
        self.cur = self.subroutine_table

    def end_subroutine(self) -> None:
        """Ends the compilation of the current subroutine, returning cur to self"""
        self.cur = self

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        if name not in self.var_table:
            if kind == "VAR":
                kind = "LOCAL"
            # get type of identifier as integer between 1 - 4
            kind_i = self.__get_kind(kind)
            # update table according to identifier index
            self.cur.var_table.append([name, type, kind, self.cur.type_count_arr[kind_i] if not kind_i == -1 else 0])

            if not kind_i == -1:
                self.cur.type_count_arr[kind_i] += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        kind = self.__get_kind(kind)
        return self.cur.type_count_arr[kind]

    def outer_var_count(self, kind: str):
        kind = self.__get_kind(kind)
        return self.cur.type_count_arr[kind]

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # find name - can be done by sorting the table for better optimization in table
        item = self.__search_for_name(name, "var")
        if not item:
            return ""
        else:
            return item[KIND]
        # let others handle name not being in table

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        item = self.__search_for_name(name, "var")
        if not item:
            return ""
        else:
            return item[TYPE]
        pass

    def outer_type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        item = self.__search_for_outer_name(name, "var")
        if not item:
            return ""
        else:
            return item[TYPE]
        pass

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        item = self.__search_for_name(name, "var")
        if not item:
            return -1
        else:
            return item[INDEX]
        pass

    def outer_index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        item = self.__search_for_outer_name(name, "var")
        if not item:
            return -1
        else:
            return item[INDEX]
        pass

    def outer_kind_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        item = self.__search_for_outer_name(name, "var")
        if not item:
            return ""
        else:
            return item[KIND]
        pass

    def search_in_cur_scope(self, name: str) -> bool:
        """searches for name in current scope"""
        item = self.__search_for_name(name, "var")
        if item:
            return True
        return False

    def search_in_out_outer(self, name: str) -> bool:
        """searches for name in outer scope"""
        item = self.__search_for_outer_name(name, "var")
        if item:
            return True
        return False

    def add_func_dec(self, name: str) -> None:
        if name not in self.cur.func_table:
            self.cur.func_table.append([name])

    def add_n_locals(self, name: str, n_locals: int) -> None:
        item = self.__search_for_name(name, "func")
        if item:
            item.append(n_locals)

    def add_n_args(self, name: str, n_args: int) -> None:
        item = self.__search_for_name(name, "func")
        if item:
            item.append(n_args)

    def n_locals_of(self, name: str) -> int:
        item = self.__search_for_name(name, "func")
        if item:
            return item[N_LOCALS]

    def n_args_of(self, name: str) -> int:
        item = self.__search_for_name(name, "func")
        if item:
            return item[N_ARGS]

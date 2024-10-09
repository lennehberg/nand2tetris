""" TEST FILE FOR CODEWRITER AND PARSER """

from Parser import Parser


def test_parser_command_type():
    file_in = open("testin.txt", 'r')
    parser = Parser(file_in)
    print(parser.command_type())
    print(parser.arg1() + " " + str(parser.arg2()))
    print(parser.has_more_commands())
    parser.advance()
    print(parser.command_type())
    print(parser.arg1() + " " + str(parser.arg2()))
    print(parser.has_more_commands())
    parser.advance()
    print(parser.command_type())
    print(parser.arg1())
    print(parser.has_more_commands())




test_parser_command_type()
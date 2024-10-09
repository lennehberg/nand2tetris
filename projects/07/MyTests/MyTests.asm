// push  constant 30000
@30000
D=A
@SP
A=M
M=D
@SP
M=M+1
// push  constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// shiftright
@SP
A=M-1
M=M>>
// pop  local 0
@0
D=A
@LCL
A=M+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R13
A=M
M=D

// function SimpleFunction.test
(SimpleFunction.test)
// push 0 n_vars
@1
D=A
(LOOPED_PUSH.0)
@SP
A=M+D
M=0
A=A+1
D=D-1
@CONT.0
D;JLT
@LOOPED_PUSH.0
0;JMP
(CONT.0)
@2
D=A
@SP
M=M+D
// push  local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push  local 1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@1
D=A
@SP
M=M-D
// not
@SP
A=M-1
M=!M
// push  argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@1
D=A
@SP
M=M-D
// push  argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@1
D=A
@SP
M=M-D
// return
// Save LCL to RAM[14]
@LCL
D=M
@R14
M=D
// Reposition the return value for the caller
@SP
A=M-1
D=M
@ARG
A=M
M=D
// Reposition SP
D=A+1
@SP
M=D
// Restores THAT to caller
@R14
A=M-1
D=M
@THAT
M=D
// Restores THIS to caller
@2
D=A
@R14
A=M-D
D=M
@THIS
M=D
// Restores ARG to the caller
@3
D=A
@R14
A=M-D
D=M
@ARG
M=D
// Restores LCL to caller
@4
D=A
@R14
A=M-D
D=M
@LCL
M=D
// goto return address
@5
D=A
@R14
A=M-D
A=M
0;JMP

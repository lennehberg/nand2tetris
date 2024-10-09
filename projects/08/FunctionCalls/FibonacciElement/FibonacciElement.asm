@256
D=A
@SP
M=D
// call Sys.init
// save n_vars to RAM[14]
@0
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Sys.init.1
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push LCL
@LCL
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push ARG
@ARG
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THIS
@THIS
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THAT
@THAT
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Sys.init
0;JMP
// return label
(Sys.init.1)
// function Main.fibonacci
(Main.fibonacci)
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
// push  constant 2
@2
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// lt
@SP
A=M-1
D=M
A=A-1
D=M-D
@SET_SP_TRUE.0
D;JLT
@SET_SP_FALSE.0
0;JMP
(SET_SP_TRUE.0)
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
M=M-1
D=-1
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
@END_SP_SET_BOOL.0
0;JMP
(SET_SP_FALSE.0)
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
M=M-1
D=0
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
(END_SP_SET_BOOL.0)
// if-goto IF_TRUE
// check stack head true of false
@SP
A=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
// goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP
// label IF_TRUE
(Main.fibonacci$IF_TRUE)
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
// return
// Save LCL to RAM[15]
@LCL
D=M
@R15
M=D
@5
D=A
@R15
A=M-D
D=M
@RET_AD
M=D
// Reposition the return value for the caller
@SP
A=M-1
D=M
@ARG
A=M
M=D
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
// Reposition SP
@ARG
D=M+1
@SP
M=D
// Restores THAT to caller
@R15
A=M-1
D=M
@THAT
M=D
// Restores THIS to caller
@2
D=A
@R15
A=M-D
D=M
@THIS
M=D
// Restores ARG to the caller
@3
D=A
@R15
A=M-D
D=M
@ARG
M=D
// Restores LCL to caller
@4
D=A
@R15
A=M-D
D=M
@LCL
M=D
// goto return address
@RET_AD
A=M
0;JMP
// label IF_FALSE
(Main.fibonacci$IF_FALSE)
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
// push  constant 2
@2
D=A
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
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
// call Main.fibonacci
// save n_vars to RAM[14]
@1
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Main.fibonacci.2
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push LCL
@LCL
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push ARG
@ARG
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THIS
@THIS
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THAT
@THAT
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Main.fibonacci
0;JMP
// return label
(Main.fibonacci.2)
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
// push  constant 1
@1
D=A
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
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
// call Main.fibonacci
// save n_vars to RAM[14]
@1
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Main.fibonacci.3
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push LCL
@LCL
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push ARG
@ARG
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THIS
@THIS
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THAT
@THAT
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Main.fibonacci
0;JMP
// return label
(Main.fibonacci.3)
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
// return
// Save LCL to RAM[15]
@LCL
D=M
@R15
M=D
@5
D=A
@R15
A=M-D
D=M
@RET_AD
M=D
// Reposition the return value for the caller
@SP
A=M-1
D=M
@ARG
A=M
M=D
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
// Reposition SP
@ARG
D=M+1
@SP
M=D
// Restores THAT to caller
@R15
A=M-1
D=M
@THAT
M=D
// Restores THIS to caller
@2
D=A
@R15
A=M-D
D=M
@THIS
M=D
// Restores ARG to the caller
@3
D=A
@R15
A=M-D
D=M
@ARG
M=D
// Restores LCL to caller
@4
D=A
@R15
A=M-D
D=M
@LCL
M=D
// goto return address
@RET_AD
A=M
0;JMP
// function Sys.init
(Sys.init)
// push  constant 4
@4
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// call Main.fibonacci
// save n_vars to RAM[14]
@1
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Main.fibonacci.4
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push LCL
@LCL
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push ARG
@ARG
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THIS
@THIS
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push THAT
@THAT
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// reposition ARG = SP - 5 - n_args (SP - 5 is saved in RAM[15])
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Main.fibonacci
0;JMP
// return label
(Main.fibonacci.4)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0;JMP

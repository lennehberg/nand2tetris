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
// function Sys.init
(Sys.init)
// push  constant 4000
@4000
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 0
@THIS
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 5000
@5000
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 1
@THAT
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// call Sys.main
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
@Sys.main.2
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
@Sys.main
0;JMP
// return label
(Sys.main.2)
// pop  temp 1
@1
D=A
@5
A=A+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// label LOOP
(Sys.init$LOOP)
// goto LOOP
@Sys.init$LOOP
0;JMP
// function Sys.main
(Sys.main)
// push 0 n_vars
@4
D=A
(LOOPED_PUSH.1)
@SP
A=M+D
M=0
A=A+1
D=D-1
@CONT.1
D;JLT
@LOOPED_PUSH.1
0;JMP
(CONT.1)
@5
D=A
@SP
M=M+D
// push  constant 4001
@4001
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 0
@THIS
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 5001
@5001
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 1
@THAT
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 200
@200
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  local 1
@1
D=A
@LCL
A=M+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 40
@40
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  local 2
@2
D=A
@LCL
A=M+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 6
@6
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  local 3
@3
D=A
@LCL
A=M+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 123
@123
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// call Sys.add12
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
@Sys.add12.3
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
@Sys.add12
0;JMP
// return label
(Sys.add12.3)
// pop  temp 0
@0
D=A
@5
A=A+D
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
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
// push  local 2
@2
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
// push  local 3
@3
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
// push  local 4
@4
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
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
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
// function Sys.add12
(Sys.add12)
// push  constant 4002
@4002
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 0
@THIS
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
// push  constant 5002
@5002
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// pop  pointer 1
@THAT
D=A
@R13
M=D
@SP
A=M-1
D=M
@R14
M=D
@1
D=A
@SP
M=M-D
@R14
D=M
@R13
A=M
M=D
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
// push  constant 12
@12
D=A
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

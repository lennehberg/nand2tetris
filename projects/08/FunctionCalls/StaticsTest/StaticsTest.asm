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
// push  constant 8
@8
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// call Class1.set
// save n_vars to RAM[14]
@2
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Class1.set.2
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
@2
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Class1.set
0;JMP
// return label
(Class1.set.2)
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
// push  constant 23
@23
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push  constant 15
@15
D=A
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// call Class2.set
// save n_vars to RAM[14]
@2
D=A
@R14
M=D
// save current address of head of stack to RAM[15], for ARG repositioning
@SP
D=M
@R15
M=D
// push return address
@Class2.set.3
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
@2
D=D-A
@ARG
M=D
// reposition LCL = SP
@SP
D=M
@LCL
M=D
// goto function name
@Class2.set
0;JMP
// return label
(Class2.set.3)
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
// call Class1.get
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
@Class1.get.4
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
@Class1.get
0;JMP
// return label
(Class1.get.4)
// call Class2.get
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
@Class2.get.5
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
@Class2.get
0;JMP
// return label
(Class2.get.5)
// label WHILE
(Sys.init$WHILE)
// goto WHILE
@Sys.init$WHILE
0;JMP
// function Class1.set
(Class1.set)
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
// pop  static 0
@Class1.0
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
// pop  static 1
@Class1.1
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
// push  constant 0
@0
D=A
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
// function Class1.get
(Class1.get)
// push  static 0
@Class1.0
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push  static 1
@Class1.1
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
// function Class2.set
(Class2.set)
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
// pop  static 0
@Class2.0
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
// pop  static 1
@Class2.1
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
// push  constant 0
@0
D=A
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
// function Class2.get
(Class2.get)
// push  static 0
@Class2.0
D=M
@SP
A=M
M=D
@1
D=A
@SP
M=M+D
// push  static 1
@Class2.1
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

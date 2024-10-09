// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here

// INIT R2, counter
    @R2
    M=0
    @counter
    M=0
    

  (MultLoop)
// if  R1 - counter == 0
// exit loop
    @R1
    D=M
    @counter
    D=D-M
    @END
    D;JEQ
    
// multiplication a*b is just a+a+a+...+a b times 
    @R0
    D=M
    @R2
    M=M+D
// increment counter 
    @counter
    M=M+1    
    @MultLoop
    0;JMP

// infinite loop
  (END)
    @END
    0;JMP

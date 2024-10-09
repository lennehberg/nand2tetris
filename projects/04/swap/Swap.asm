// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
// init varialbe
@R14
D=M
@minAdd // init min address to the first address of the array
M=D
A=M // shift A register to the first address of the array
D=M
@minVal // init the min val to the first value of the array
M=D

// do the same as above for max
@R14
D=M
@maxAdd // init min address to the first address of the array
M=D
A=M // shift the A register to the first address of the array
D=M
@maxVal // inint the max bal to the first value of the array
M=D

@TEMPVAL
M=0 // init a temp value variable
@TEMPADD
M=0 // init a temp address variable

@counter
M=0 // init counter to 0

(MMLOOP) // iterate over the array, changing min and max accordingly
  @counter
  D=M-1
  @R15
  D=D-M
  @ENDMMLOOP // if counter == array_len - 1 exit loop
  D;JEQ
  
  // get address of array[counter]
  @counter
  D=M // D holds counter for array[counter]
  @R14
  A=M+D // moves the A register to the address of array[counter]
        // (MEMORY[RAM[14] + counter]
  // store the address of the value in TEMPADD 
  // and the value itself in TEMPVAL
  D=A  
  @TEMPADD
  M=D // stores the address of the current value
  A=M // sets the A register to the address of the value
  D=M // sets the value of the D register to the current value
  @TEMPVAL
  M=D // stores the current value in TEMPVAL

  @minVal
  D=M-D // check if currentVal - minVal =< 0 
	// (currentVal =< minVal)
  // if D < minVal then minVal = D, minAdd = Memory[A]
  @newMin
  D;JLE

  @TEMPVAL
  D=M
  @maxVal
  D=M-D // check if currentVal - maxVal => 0
	// (currentVal => maxVal
  @newMax
  D;JGE
(CONT)
  @counter
  M=M+1
  @MMLOOP
  0;JMP    
(ENDMMLOOP)

@TEMPVAL // reset temp value
M=0

@minVal 
D=M
@TEMPVAL // store min value in temp value
M=D

@maxVal
D=M
@minAdd // store max value in address of min value
A=M
M=D
@TEMPVAL // get min value from temp
D=M
@maxAdd // store min value in max address
A=M
M=D
@END
0;JMP


(newMin)
  // sets the minVal to TEMPVAL and minAdd to TEMPADD
  @TEMPVAL
  D=M
  @minVal
  M=D
  @TEMPADD
  D=M
  @minAdd
  M=D
  @CONT
  0;JMP

(newMax)
  // sets the maxVal to TEMPVAL and maxAdd to TEMPADD
  @TEMPVAL
  D=M
  @maxVal
  M=D
  @TEMPADD
  D=M
  @maxAdd
  M=D
  @CONT
  0;JMP

(END)
  @END
  0;JMP

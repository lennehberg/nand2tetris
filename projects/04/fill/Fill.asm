// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

// Put your code here.

  (LOOP)
    // init variable
    @r
    M=0
    @c
    M=0
    @counter
    M=0
    // if RAM[24576] == 0 => no key is pressed, 
    // write "white" to every pixel
    @KBD
    D=M
    @white
    D;JEQ
   // if RAM[24567] != 0 => a key is pressed,
   // write "black: to every pixel
   @black
   D;JNE


     (white)
       (WhiteLoop)
	 @counter 
	 D=M
	 @SCREEN
	 A=A+D
	 M=0 // sets all pixels in 16bit segments of rows to white
         @counter // go to the next set of 16bit segment of rows
	 M=M+1
	 @c // increment cols counter by 1
         M=M+1
	 // if c == 32 set c = 0 and increment r
	 @32
	 D=A // get the difference between c and 32
         @c
         D=M-D
	 @notincrow
	 D;JNE // if D!=0 then dont increment r and dont reset c
	 @r
         M=M+1
	 @256
	 D=A // if rows reached 256, no more rows to change, end white loop
         @r
         D=M-D
	 @EndWhite
	 D;JEQ
	 @c // start from col segment 0 at new row
	 M=0
         (notincrow)
	 @WhiteLoop
	 0;JMP
       (EndWhite) 
       @LOOP
       0;JMP

     (black)
       (BlackLoop)
	 @counter
	 D=M
 	 @SCREEN
	 A=A+D
         M=-1 // sets all pixels in 16bit segments of rows to white
	 @counter
	 M=M+1
	 @c
	 M=M+1
	 @32
         D=A // get the difference between c and 32
	 @c
	 D=M-D
         @notincrowb
         D;JNE // if D!=0 then dont increment r and dont reset c
         @r
	 M=M+1
         @256
         D=A // if rows reached 256, no more rows to change, end white loop
	 @r
	 D=M-D
         @EndBlack
         D;JEQ
         @c // start from col segment 0 at new row
	 M=0
         (notincrowb)
	 @BlackLoop
	 0;JMP
       (EndBlack)
    
    @LOOP
    0;JMP
(END)
@END
0;JMP	     

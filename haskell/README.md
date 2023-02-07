# conway.hs

This has an infinite board. It can display the smallest rectangular segment required to contain all currently live cells,
or the contents of any fixed rectangle.
It does not take any sort of user input; to modify it, you must modify the code and recompile it with GHC.

The `main` function determines what will be run when you execute it.
There are three sample boards, `glider`, `gliderBoard`, and `pentomino`. 
* `glider` contains a single glider, which will not appear to move as the display will move with it.
* `gliderBoard` contains a glider plus two squares to anchor the display. The glider will move until it hits one square
    and they mutually annihilate, leaving the display covering only the other square.
* `pentomino` contains an r-pentomino, which takes 1103 steps to stabilize. However, its stable form includes gliders which
    will continue to expand the display to an unlimited extent if used with `displayLive`.

There are several relevant functions for execution and output:
* `step` executes a single step on a board.
* `run` takes an integer and runs that many steps.
* `displayLive` sends a display of all live cells in the board to standard output.
* `runLive` takes an integer and runs that many steps, displaying the board after each step.
* `displayWindow` takes pairs of max/min values for x and y, and displays that window of the board.
* `runWindow` takes pairs of max/min values for x and y and an integer, and runs that many steps, displaying that window after each step.

# refined.hs

This is intended to be a more elegant version, using maps rather than sets. Only live display is available,
but it does have a function which can turn arbitrary strings into boards (by character ord; this has its limits but isn't worthless)
and takes a command line argument of a file to read. glider.txt makes a glider, pentomino.txt makes a pentomino, etc.
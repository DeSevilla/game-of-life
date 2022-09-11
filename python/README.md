
#  Conway.py

This uses a finite, square board of customizable size. 
It takes commands from user input which can modify the state of the board.

## How to Play

On starting the game, it will generate a 20x20 empty board.
The state of the board can be modified with commands and then run or stepped through.
Commands can be chained together with semicolons.
The state of the board will be displayed after each command.

You can record sequences of commands as macros. Macros are saved in macros.json.
The starting macros are `glider` (creates a glider in the top left, assuming it is empty)
and `genesis` (fills the board with random soup then runs for 100 turns with 0.15 delay).

The commands are:
* `stop` - exit the program
* `step [<n>]` - take n game steps without displaying intermediate results; if n is omitted it will be 1
* `run <n> [<d>]` - run and display n game steps with a delay of d; if d is omitted it will be 0.3
* `flip <x> <y>` - flip the state at cell (x, y)
* `board <n>` - set the board to be an empty n by n square
* `soup [<n>]` - set the board to be an n by n square with random contents. If n is omitted it will be the current board size.
* `record` - begin recording a macro
* `end <name>` - saves the current macro as name. It can then be invoked as a command.
* `help` - prints a help message. This is mostly redundant with this document but will contain a list of extant macros.


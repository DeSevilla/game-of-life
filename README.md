# Introduction

This is a couple of simple implementations of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
The game itself is very simple. 
It requires no players, instead evolving according to specified rules from a starting configuration.
The board is divided into cells which can be "alive" or "dead".
At each step, each cell evolves based on its state and its neighbors' states.

# Game Rules:

1. An alive cell with either two or three neighbors stays alive.
2. A dead cell with exactly three live neighbors becomes alive.
3. All other cells die (if alive) or stay dead.

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

# Conway.hs

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

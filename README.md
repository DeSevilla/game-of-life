# Introduction

This is a simple Python implementation of [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
The game itself is very simple. 
It requires no players, instead evolving according to specified rules from a starting configuration.
The board is divided into cells which can be "alive" or "dead".
At each step, each cell evolves based on its state and its neighbors' states.

# Game Rules:

1. An alive cell with either two or three neighbors stays alive.
2. A dead cell with exactly three live neighbors becomes alive.
3. All other cells die (if alive) or stay dead.

# How to Interact

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

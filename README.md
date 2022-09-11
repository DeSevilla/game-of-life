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

Beyond these basic rules, the implementations differ in many ways. Each specific implementation has its own README. 
The implementations are in [Haskell](/haskell/README.md), [Python](/python/README.md), and [Rust](/rust/README.md).
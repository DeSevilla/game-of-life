import numpy as np
import random, json, time

class GameOfLifeFinite:
    def __init__(self, size):
        self.board = self.make_board(size)

    def step(self):
        new_array = [0] * len(self.board)
        for i, row in enumerate(new_array):
            new_array[i] = [False] * len(self.board[0])  # assumes the array is at least 1x1
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                neighbors = {True: 0, False: 0}
                if i > 0:
                    neighbors[self.board[i-1][j]] += 1
                    if j > 0:
                        neighbors[self.board[i-1][j-1]] += 1
                    if j < len(self.board[0]) - 1:
                        neighbors[self.board[i-1][j+1]] += 1
                if j > 0:
                    neighbors[self.board[i][j-1]] += 1
                    if i < len(self.board) - 1:
                        neighbors[self.board[i+1][j-1]] += 1
                if i < len(self.board) - 1:
                    neighbors[self.board[i+1][j]] += 1
                    if j < len(self.board[0]) - 1:
                        neighbors[self.board[i+1][j+1]] += 1
                if j < len(self.board[0]) - 1:
                    neighbors[self.board[i][j+1]] += 1
                if cell:
                    if neighbors[True] < 2:
                        new_array[i][j] = False
                    elif neighbors[True] > 3:
                        new_array[i][j] = False
                    else:
                        new_array[i][j] = True
                else:
                    if neighbors[True] == 3:
                        new_array[i][j] = True
                    else:
                        new_array[i][j] = False
        return new_array

    def repl(self):
        commands = []
        recording = False
        with open('macros.json', 'r') as macros_file:
            macros = json.load(macros_file)
        current_macro = []
        while True:
            self.print_board()
            if not commands:
                control = input('Enter command or "help": ')
                commands = [comm.strip() for comm in control.split(';')]
            else:
                print(commands[0])
            if recording:
                current_macro.append(commands[0])
            argc = commands[0].split(' ')
            if argc[0] == "help" or argc[0] == '"help"':
                print("For more information, see README.md")
                print("Commands can be chained together with ;")
                print("COMMAND LIST:")
                print("stop - exit the program")
                print("step [<n>] - take <n> game steps; if n is omitted it will be 1")
                print("run <n> [<d>] - display n game steps with a delay of d; if d is omitted it will be 1")
                print("flip <x> <y> - flip the state at cell (x, y)")
                print("board <n> - set the board to be an empty n by n square")
                print("soup <n> - set the board to be an n by n square with random contents")
                print("record - begin recording a macro")
                print("end <name> - saves the current macro as <name>. It can then be invoked as a command.")
                print(f"Current macros: {', '.join(m for m in macros)}")
                print("help - print this message")
            elif argc[0] == 'step':
                if len(argc) > 2:
                    print('Usage: step [<n>]')
                elif len(argc) == 2:
                    n = int(argc[1])
                    for i in range(n):
                        self.board = self.step()
                else:
                    self.board = self.step()
            elif argc[0] == 'run':
                if len(argc) > 3 or len(argc) < 2:
                    print("Usage: run <n> [<d>]")
                else:
                    n = int(argc[1])
                    if len(argc) == 3:
                        d = float(argc[2])
                    else:
                        d = 0.3
                    for i in range(n):
                        print(i + 1)
                        self.board = self.step()
                        if i < n - 1:
                            self.print_board()
                            time.sleep(d)
            elif argc[0] == 'flip':
                try:
                    x = int(argc[1])
                    y = int(argc[2])
                    self.board[x][y] = not self.board[x][y]
                except ValueError:
                    print(f'Could not parse {argc[1]} and {argc[2]} as integers')
                except IndexError:
                    print('Not a point on the board!')
            elif argc[0] == 'board':
                self.board = self.make_board(int(argc[1]))
            elif argc[0] == 'soup':
                if len(argc) > 2:
                    print('Usage: soup [<n>]')
                else:
                    if len(argc) == 2:
                        size = argc[1]
                    else:
                        size = len(self.board)
                    self.board = self.make_board(int(size), soup=True)
            elif argc[0] == 'record':
                recording = True
            elif argc[0] == 'end':
                if recording:
                    recording = False
                    macros[argc[1]] = ';'.join(current_macro[:-1])  # [:-1] drops the end macro command
                    with open('macros.json', 'w') as macros_file:
                        json.dump(macros, macros_file)
                    current_macro = ''
                else:
                    print("Not currently recording")
            elif argc[0] == "stop" or argc[0] == "quit":
                break
            elif argc[0] in macros:
                commands = [commands[0]] + [c.strip() for c in macros[argc[0]].split(';')] + commands[1:]
            else:
                print("Not a valid command")
            commands = commands[1:]

    def print_board(self):
        board_str = '   ' + ' '.join([str(int(i / 10)) for i in range(len(self.board))]) + '\n'
        board_str += '   ' + ' '.join([str(i % 10) for i in range(len(self.board))]) + '\n'
        for i, row in enumerate(self.board):
            board_str += f'{i:2} ' + ' '.join(['▮' if cell else '.' for cell in row]) + '\n'
        print(board_str, end=None)

    def make_board(self, n, soup=False):
        board = np.empty(shape=(n, n), dtype=np.bool_)
        for i, row in enumerate(board):
            if soup:
                board[i] = [random.randint(0, 1) == 0 for _ in range(n)]
            else:
                board[i] = [False] * n
        return board


def neighbors(p):
    return {(p[0] + dx, p[1] + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx != 0 or dy != 0)}

def adjacent(p1, p2):
    return abs(p1[0] - p2[0]) <= 1 or abs(p1[0] - p2[0]) <= 1

class GameOfLifeInfinite:
    def __init__(self, points: set):
        self.board = points
        self.displayAll = True
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def step(self):
        new_board = set()
        for point in set.union(*[neighbors(p) for p in self.board]):
            live = len(self.board.intersection(neighbors(point)))
            if live == 3:
                new_board.add(point)
            elif live == 2 and point in self.board:
                new_board.add(point)
        self.board = new_board

    def print_board(self):
        if self.displayAll:
            if self.board:
                xs = [p[0] for p in self.board]
                self.min_x = min(xs)
                self.max_x = max(xs)
                ys = [p[1] for p in self.board]
                self.min_y = min(ys)
                self.max_y = max(ys)
            else:
                self.min_x = 0
                self.min_y = 0
                self.max_x = 0
                self.max_y = 0
        board_str = '   ' + ' '.join([str(int(abs(i) / 10)) for i in range(self.min_x, self.max_x+1)]) + '\n'
        board_str += '   ' + ' '.join([str(abs(i) % 10) for i in range(self.min_x, self.max_x+1)]) + '\n'
        rows = [['▮' if (x, y) in self.board else '.' for x in range(self.min_x, self.max_x+1)] 
                for y in range(self.min_y, self.max_y+1)]
        for i, row in enumerate(rows):
            board_str += f'{abs(self.min_y + i):2} ' + ' '.join(row) + '\n'
        print(board_str, end=None)

    def repl(self):
        commands = []
        current_macro = []
        recording = False
        with open('macros_infinite.json', 'r') as macros_file:
            macros = json.load(macros_file)
        while True:
            self.print_board()
            if not commands:
                control = input("Enter command: ")
                commands = [comm.strip() for comm in control.split(';')]
            else:
                print(commands[0])
            if recording:
                current_macro.append(commands[0])
            argc = commands[0].split(' ')
            if argc[0] == "help" or argc[0] == '"help"':
                print("For more information, see README.md")
                print("Commands can be chained together with ;")
                print("COMMAND LIST:")
                print("stop - exit the program")
                print("step [<n>] - take <n> game steps; if n is omitted it will be 1")
                print("run <n> [<d>] - display n game steps with a delay of d; if d is omitted it will be 1")
                print("live <x> <y> - set cell (x, y) to be live")
                print("dead <x> <y> - set cell (x, y) to be dead")
                print("clear - clear all live cells from the board")
                print("window [live] [<xmin> <xmax> <ymin> <ymax>] - Sets the window to be printed. "
                      "'live' will include all live cells; otherwise specify a rectangular range.")
                print("record - begin recording a macro")
                print("end <name> - saves the current macro as <name>. It can then be invoked as a command.")
                print(f"Current macros: {', '.join(m for m in macros)}")
                print("help - print this message")
            elif argc[0] == 'step':
                if len(argc) > 2:
                    print('Usage: step [<n>]')
                elif len(argc) == 2:
                    n = int(argc[1])
                    for i in range(n):
                        self.step()
                else:
                    self.step()
            elif argc[0] == 'run':
                if len(argc) > 3 or len(argc) < 2:
                    print("Usage: run <n> [<d>]")
                else:
                    n = int(argc[1])
                    if len(argc) == 3:
                        d = float(argc[2])
                    else:
                        d = 0.3
                    for i in range(n):
                        print(i + 1)
                        self.step()
                        if i < n - 1:
                            self.print_board()
                            time.sleep(d)
            elif argc[0] == 'live':
                try:
                    x = int(argc[1])
                    y = int(argc[2])
                    self.board.add((x, y))
                except ValueError:
                    print(f'Could not parse {argc[1]} and {argc[2]} as integers')
                except IndexError:
                    print("Usage - live <x> <y>")
            elif argc[0] == 'dead':
                try:
                    x = int(argc[1])
                    y = int(argc[2])
                    self.board.remove((x, y))
                except ValueError:
                    print(f'Could not parse {argc[1]} and {argc[2]} as integers')
                except IndexError:
                    print("Usage - dead <x> <y>")
            elif argc[0] == 'clear':
                if len(argc) > 1:
                    print("clear does not take arguments")
                else:
                    self.board = set()
            elif argc[0] == "window":
                if len(argc) == 2 and argc[1] == 'live':
                    self.displayAll = True
                elif len(argc) == 5:
                    try:
                        self.displayAll = False
                        self.min_x = int(argc[1])
                        self.max_x = int(argc[2])
                        self.min_y = int(argc[3])
                        self.max_y = int(argc[4])
                    except ValueError:
                        print("Could not interpret arguments as integers")
                else:
                    print("Usage - window [live] [<minX> <maxX> <minY> <maxY>]")
            elif argc[0] == 'record':
                recording = True
            elif argc[0] == 'end':
                if recording:
                    print(f"Ending macro of length {len(current_macro)}")
                    recording = False
                    macros[argc[1]] = ';'.join(current_macro[:-1])  # [:-1] drops the end macro command
                    with open('macros_infinite.json', 'w') as macros_file:
                        json.dump(macros, macros_file)
                    current_macro = ''
                else:
                    print("Not currently recording")
            elif argc[0] == "stop" or argc[0] == "quit":
                break
            elif argc[0] in macros:
                commands = [commands[0]] + [c.strip() for c in macros[argc[0]].split(';')] + commands[1:]
            else:
                print("Not a valid command")
            commands = commands[1:]

if __name__ == '__main__':
    pentomino = {(0, 0), (0, 1), (0, 2), (1, 2), (-1, 1)}
    game = GameOfLifeInfinite(pentomino)
    game.repl()

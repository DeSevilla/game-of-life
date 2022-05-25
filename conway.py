import numpy as np
import random, json, time

def step(array):
    new_array = [0] * len(array)
    for i, row in enumerate(new_array):
        new_array[i] = [False] * len(array[0])  # assumes the array is at least 1x1
    for i, row in enumerate(array):
        for j, cell in enumerate(row):
            neighbors = {True: 0, False: 0}
            if i > 0:
                neighbors[array[i-1][j]] += 1
                if j > 0:
                    neighbors[array[i-1][j-1]] += 1
                if j < len(array[0]) - 1:
                    neighbors[array[i-1][j+1]] += 1
            if j > 0:
                neighbors[array[i][j-1]] += 1
                if i < len(array) - 1:
                    neighbors[array[i+1][j-1]] += 1
            if i < len(array) - 1:
                neighbors[array[i+1][j]] += 1
                if j < len(array[0]) - 1:
                    neighbors[array[i+1][j+1]] += 1
            if j < len(array[0]) - 1:
                neighbors[array[i][j+1]] += 1
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

def repl(board):
    commands = []
    recording = False
    with open('macros.json', 'r') as macros_file:
        macros = json.load(macros_file)
    current_macro = []
    while True:
        print_board(board)
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
                    board = step(board)
            else:
                board = step(board)
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
                    board = step(board)
                    if i < n - 1:
                        print_board(board)
                        time.sleep(d)
        elif argc[0] == 'flip':
            try:
                x = int(argc[1])
                y = int(argc[2])
                board[x][y] = not board[x][y]
            except ValueError:
                print(f'Could not parse {argc[1]} and {argc[2]} as integers')
            except IndexError:
                print('Not a point on the board!')
        elif argc[0] == 'board':
            board = make_board(int(argc[1]))
        elif argc[0] == 'soup':
            if len(argc) > 2:
                print('Usage: soup [<n>]')
            else:
                if len(argc) == 2:
                    size = argc[1]
                else:
                    size = len(board)
                board = make_board(int(size), soup=True)
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
        elif argc[0] == "stop":
            break
        elif argc[0] in macros:
            commands = [commands[0]] + [c.strip() for c in macros[argc[0]].split(';')] + commands[1:]
        else:
            print("Not a valid command")
        commands = commands[1:]

def print_board(board):
    board_str = '  ' + ' '.join([str(i % 10) for i in range(len(board))]) + '\n'
    for i, row in enumerate(board):
        board_str += f'{i % 10} ' + ' '.join(['▮' if cell else '.' for cell in row]) + '\n'
    print(board_str, end=None)

# def print_board(board):
#     win = GraphWin('Game of Life', len(board) * 10, len(board[0]) * 10)
#     win.setCoords(0, 0, len(board), len(board[0]))
#     for i in range(len(board)):
#         for j in range(len(board[0])):
#             cell = Rectangle(Point(i, i+1), Point(j, j+1))
#             cell.draw(win)
#     win.getMouse()

def make_board(n, soup=False):
    board = np.empty(shape=(n, n), dtype=np.bool_)
    for i, row in enumerate(board):
        if soup:
            board[i] = [random.randint(0, 1) == 0 for _ in range(n)]
        else:
            board[i] = [False] * n
    return board
 

if __name__ == '__main__':
    repl(make_board(20))

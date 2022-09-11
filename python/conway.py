import numpy as np
import random
import json
import time
import pygame


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
                print("stop/quit - exit the program")
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
                    current_macro = []
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


class GameOfLifeInfinite:
    def __init__(self, points: set = None, display_all=False, display_type='game'):
        if points is None:
            self.board = set()
        else:
            self.board = points
        self.display_all = display_all
        self.expected_height = 512
        self.min_x = -50
        self.max_x = 50
        self.min_y = -50
        self.max_y = 50
        self.display_type = display_type
        if self.display_type == 'game':
            self.text_output = []
            pygame.init()
            self.window = pygame.display.set_mode((self.expected_height, self.expected_height), pygame.RESIZABLE)
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 24)
            self.max_width = 1024
            

    def step(self):
        if self.board:
            new_board = set()
            for point in set.union(*[neighbors(p) for p in self.board]):
                live = len(self.board.intersection(neighbors(point)))
                if live == 3:
                    new_board.add(point)
                elif live == 2 and point in self.board:
                    new_board.add(point)
            self.board = new_board

    def size_board(self):
        if self.display_all:
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

    def get_input(self, string):
        if self.display_type == 'game':
            return self.game_input(string)
        else:
            return input(string)
    
    def send_output(self, string):
        if self.display_type == 'game':
            self.game_output(string)
        else:
            print(string)
    
    def game_output(self, string):
        print(string)
        self.text_output += [string]
        self.show_board()
            
    def game_input(self, prompt):
        self.game_output(prompt)
        done = False
        result = ''
        self.text_output.append(result)
        while not done:
            changed = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE and len(result) > 0:
                        result = result[:-1]
                        changed = True
                    else:
                        result += event.unicode
                        changed = True
            if changed:
                self.text_output[-1] = result
                self.show_board()
        return result

    def game_board(self):
        self.size_board()
        x_range = self.max_x + 1 - self.min_x
        y_range = self.max_y + 1 - self.min_y
        aspect_ratio = x_range / y_range
        scale_factor = int(self.expected_height / y_range)
        # print(scale_factor)
        def scale_x(n):
            return (n - self.min_x) * scale_factor
        def scale_y(n):
            return (n - self.min_y) * scale_factor
        data = np.zeros((x_range * scale_factor, y_range * scale_factor, 3), dtype=np.uint8)
        for (x, y) in filter(lambda pair: self.min_x <= pair[0] <= self.max_x and self.min_y <= pair[1] <= self.max_y, self.board):
            # print('x', scale_x(x), scale_x(x+1))
            # print('y', scale_y(y), scale_y(y+1))
            data[scale_x(x):scale_x(x+1),scale_y(y):scale_y(y+1)] = [255, 255, 255]
        if self.expected_height * aspect_ratio > self.max_width:
            display_height = int(self.max_width / aspect_ratio)
        else:
            display_height = self.expected_height
        self.window = pygame.display.set_mode((int(display_height * aspect_ratio), display_height))
        self.window.fill((0, 0, 0))
        surface = pygame.pixelcopy.make_surface(data)
        self.window.blit(surface, (0, 0))
        for i, text in enumerate(self.text_output):
            text_surface = self.font.render(text, True, pygame.Color('lightskyblue3'))
            self.window.blit(text_surface, (0, i * 24 + 10))
        self.text_output = self.text_output[-3:]
        pygame.display.flip()
        # img = Image.fromarray(data)
        # pygame.image.fromstring(img.tobytes(), img.size, img.mode).convert()
        # img.show()

   
    def print_board(self, live_value='X', dead_value='.'):
        self.size_board()
        rows = [[live_value if (x, y) in self.board else dead_value for x in range(self.min_x, self.max_x+1)] 
                for y in range(self.min_y, self.max_y+1)]

        board_str = '   ' + ' '.join([str(int(abs(i) / 10)) for i in range(self.min_x, self.max_x+1)]) + '\n'
        board_str += '   ' + ' '.join([str(abs(i) % 10) for i in range(self.min_x, self.max_x+1)]) + '\n'
        for i in range(self.max_y, self.min_y - 1, -1):
            board_str += f'{abs(i):2} ' + ' '.join(rows[i - self.min_y]) + '\n'
        print(board_str, end=None)
 
    def show_board(self):
        if self.display_type == 'print':
            return self.print_board()
        elif self.display_type == 'game':
            return self.game_board()
        else:
            raise ValueError('type must be either print or game')

    def repl(self, starting_commands=None):
        if starting_commands is None:
            commands = []
        else:
            commands = starting_commands
        current_macro = []
        recording = False
        with open('macros_infinite.json', 'r') as macros_file:
            macros = json.load(macros_file)
        while True:
            self.show_board()
            if not commands:
                control = self.get_input("Enter command or 'help': ")
                commands = [comm.strip() for comm in control.split(';')]
            else:
                self.send_output(commands[0])
            if recording:
                current_macro.append(commands[0])
            argc = commands[0].split(' ')
            if argc[0] == "help" or argc[0] == '"help"':
                self.send_output("For more information, see README.md")
                self.send_output("Commands can be chained together with ;")
                self.send_output("COMMAND LIST:")
                self.send_output("stop/quit - exit the program")
                self.send_output("step [<n>] - take <n> game steps; if n is omitted it will be 1")
                self.send_output("run <n> [<d>] - display n game steps with a delay of d; if d is omitted it will be 1")
                self.send_output("live <x> <y> - set cell (x, y) to be live")
                self.send_output("dead <x> <y> - set cell (x, y) to be dead")
                self.send_output("soup [<minX> <maxX> <minY> <maxY>] - fill the current or specified window with random values (density 0.5)")
                self.send_output("clear - clear all live cells from the board")
                self.send_output("window (live|fix) [<xmin> <xmax> <ymin> <ymax>] - Sets the window to be printed. "
                      "'live' will include all live cells; 'fix' alone will fix the current window, or "
                      "can also take a rectangular range.")
                self.send_output("record - begin recording a macro")
                self.send_output("end <name> - saves the current macro as <name>. It can then be invoked as a command.")
                self.send_output(f"Current macros: {', '.join(m for m in macros)}")
                self.send_output("help - print this message")
            elif argc[0] == 'step':
                if len(argc) > 2:
                    self.send_output('Usage: step [<n>]')
                elif len(argc) == 2:
                    n = int(argc[1])
                    for i in range(n):
                        self.step()
                else:
                    self.step()
            elif argc[0] == 'run':
                if len(argc) > 3 or len(argc) < 2:
                    self.send_output("Usage: run <n> [<d>]")
                else:
                    n = int(argc[1])
                    if len(argc) == 3:
                        d = float(argc[2])
                    else:
                        d = 0.3
                    for i in range(n):
                        self.send_output(str(i + 1))
                        self.step()
                        if i < n - 1:
                            self.show_board()
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
                except KeyError:
                    print(f"({argc[1]}, {argc[2]}) is not live")
                except IndexError:
                    print("Usage - dead <x> <y>")
            elif argc[0] == 'soup':
                if len(argc) == 5:
                    min_x = int(argc[1])
                    max_x = int(argc[2])
                    min_y = int(argc[3])
                    max_y = int(argc[4])
                else:
                    min_x = self.min_x
                    max_x = self.max_x
                    min_y = self.min_y
                    max_y = self.max_y
                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        if random.randint(0, 1) == 0:
                            self.board.add((x, y))
            elif argc[0] == 'clear':
                if len(argc) > 1:
                    print("clear does not take arguments")
                else:
                    self.board = set()
            elif argc[0] == "window":
                if argc[1] == 'live':
                    self.display_all = True
                elif argc[1] == 'fix':
                    self.display_all = False
                    if len(argc) == 6:
                        try:
                            self.min_x = int(argc[2])
                            self.max_x = int(argc[3])
                            self.min_y = int(argc[4])
                            self.max_y = int(argc[5])
                        except ValueError:
                            print("Could not interpret arguments as integers")
                    elif len(argc) != 2:
                        print("Usage - window (live|fix) [<minX> <maxX> <minY> <maxY>]")
                elif argc[1] == 'range':
                    if self.board:
                        xs = [p[0] for p in self.board]
                        ys = [p[1] for p in self.board]
                        print(min(xs), max(xs), min(ys), max(ys))
                    else:
                        print(0, 0, 0, 0)
                else:
                    print("Usage - window (live|fix) [<minX> <maxX> <minY> <maxY>]")
            elif argc[0] == 'record':
                recording = True
            elif argc[0] == 'end':
                if recording:
                    recording = False
                    macros[argc[1]] = ';'.join(current_macro[:-1])  # [:-1] drops the end macro command
                    with open('macros_infinite.json', 'w') as macros_file:
                        json.dump(macros, macros_file)
                    current_macro = []
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
    game = GameOfLifeInfinite()
    # game.repl(starting_commands=["pentomino", "window live", "run 20 0.15"])
    game.repl()

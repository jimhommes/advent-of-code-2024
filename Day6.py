from aocd import *
from time import perf_counter
import networkx as nx


class Board:
    def __init__(self, inp):
        self.board = nx.DiGraph()
        self.matrix_ids = list()
        self.id_counter = 1
        self.obstacles = []

        spl = inp.split('\n')
        for y in range(len(spl)):
            self.matrix_ids.append([-1] * len(spl[0]))
            for x in range(len(spl[0])):
                if spl[y][x] == '#':
                    self.add_obstacle(x, y)
                elif spl[y][x] == '^' or spl[y][x] == '>' or spl[y][x] == 'v' or spl[y][x] == '<':
                    self.guard = Guard(x, y, spl[y][x])

        self.add_edges()

    def add_obstacle(self, x, y):
        if self.matrix_ids[y][x] == -1:
            self.board.add_node(self.id_counter)
            self.id_counter += 1
            self.obstacles.append((x, y, self.id_counter))

    def add_edges(self):
        # Add guard edge to obstacle
        if self.guard.x_dir == 0:
            obstacles_on_guard_path = [(abs(i[1] - self.guard.y), i[3]) for i in self.obstacles if
                                     i[0] == self.guard.x and i[1] > self.guard.y * self.guard.y_dir]
        else:
            obstacles_on_guard_path = [(abs(i[0] - self.guard.x), i[3]) for i in self.obstacles if
                                     i[1] == self.guard.y and i[0] > self.guard.x * self.guard.x_dir]
        obstacles_on_guard_path.sort(key=lambda i: i[0])
        self.board.add_edge(0, obstacles_on_guard_path[0][1], weight=obstacles_on_guard_path[0][0])

        # Add all edges between obstacles
        for obstacle in self.obstacles:
            pass #TODO


class Guard:
    def __init__(self, x, y, guardchr):
        self.x = x
        self.y = y
        if guardchr == '^':
            self.x_dir = 0
            self.y_dir = -1
        elif guardchr == 'v':
            self.x_dir = 0
            self.y_dir = 1
        elif guardchr == '>':
            self.x_dir = 1
            self.y_dir = 0
        elif guardchr == '<':
            self.x_dir = -1
            self.y_dir = 0




# data_input = get_data(day=6, year=2024)
data_input = '....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#...'

t1_start = perf_counter()
board = Board(data_input)
ex2_res = 0
while True:
    board.is_guard_in_loop_on_turn_right()
    if board.move():
        break
t1_stop = perf_counter()

ex1_res = len(set(board.visited_coordinates_withoutdir))
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex1_res, part='a', day=6, year=2024)

ex2_res = len(set(board.extra_obstacle_coords))
print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex2_res, part='b', day=6, year=2024)


from aocd import *
from time import perf_counter


class Board:
    def __init__(self, inp):
        self.guard = None
        self.obstacles = []
        spl = inp.split('\n')
        self.y_length = len(spl)
        self.x_length = len(spl[0])

        for row in range(len(spl)):
            for col in range(len(spl[row])):
                if spl[row][col] == '#':
                    self.obstacles.append(Obstacle(row, col))
                elif spl[row][col] == '^' or spl[row][col] == '>' or spl[row][col] == 'v' or spl[row][col] == '<':
                    self.guard = Guard(spl[row][col], row, col)

    def move(self):
        next_guard_position_x, next_guard_position_y = self.guard.peek_move()
        if self.out_of_bounds(next_guard_position_x, next_guard_position_y):
            return True
        if self.in_obstacle(next_guard_position_x, next_guard_position_y):
            self.guard.turn()
            return False
        else:
            return self.guard.move()

    def out_of_bounds(self, x, y):
        return x < 0 or x >= self.x_length or y < 0 or y >= self.y_length

    def in_obstacle(self, x, y):
        return (x, y) in zip([obst.x for obst in self.obstacles], [obst.y for obst in self.obstacles])


class Guard:
    def __init__(self, char, y, x):
        self.y = y
        self.x = x
        if char == '^':
            self.y_dir = -1
            self.x_dir = 0
        elif char == '>':
            self.y_dir = 0
            self.x_dir = 1
        elif char == 'v':
            self.y_dir = 1
            self.x_dir = 0
        elif char == '<':
            self.y_dir = 0
            self.x_dir = -1
        self.visited_coordinates_with_dir = [(self.x, self.y, self.x_dir, self.y_dir)]
        self.visited_coordinates = [(self.x, self.y)]

    def turn(self):
        new_x_dir, new_y_dir = self.peek_turn()
        self.x_dir = new_x_dir
        self.y_dir = new_y_dir

    def peek_move(self):
        return self.x + self.x_dir, self.y + self.y_dir

    def peek_turn(self):
        if self.x_dir == 1:
            return 0, 1
        elif self.y_dir == 1:
            return -1, 0
        elif self.x_dir == -1:
            return 0, -1
        elif self.y_dir == -1:
            return 1, 0

    def move(self):
        self.x += self.x_dir
        self.y += self.y_dir
        coord = (self.x, self.y, self.x_dir, self.y_dir)
        if coord in self.visited_coordinates:
            return True
        else:
            self.visited_coordinates_with_dir.append(coord)
            self.visited_coordinates.append((self.x, self.y))
            return False

    def can_be_blocked(self):
        new_x_dir, new_y_dir = self.peek_turn()
        if new_x_dir == 0:
            return len([i for i in self.visited_coordinates_with_dir if i[0] == self.x and i[2] == new_x_dir and i[3] == new_y_dir]) > 0
        else:
            return len([i for i in self.visited_coordinates_with_dir if i[1] == self.y and i[2] == new_x_dir and i[3] == new_y_dir]) > 0

    def __repr__(self):
        return 'G(' + str(self.x) + ',' + str(self.y) + ')'


class Obstacle:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __repr__(self):
        return 'Obst(' + str(self.x) + ',' + str(self.y) + ')'


data_input = get_data(day=6, year=2024)
# data_input = '....#.....\n.........#\n..........\n..#.......\n.......#..\n..........\n.#..^.....\n........#.\n#.........\n......#...'

t1_start = perf_counter()
board = Board(data_input)
ex2_res = 0
while not board.move():
    ex2_res += board.guard.can_be_blocked()
t1_stop = perf_counter()

ex1_res = len(set(board.guard.visited_coordinates))
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex1_res, part='a', day=6, year=2024)

print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex2_res, part='b', day=6, year=2024)


from aocd import *
from time import perf_counter


class Board:

    def __init__(self, inp):
        self.guard = None
        self.obstacles = []
        spl = inp.split('\n')
        self.y_length = len(spl)
        self.x_length = len(spl[0])
        self.visited_coordinates_current = []
        self.visited_coordinates_withoutdir = []
        self.extra_obstacle_coords = []
        self.move_counter = 0

        for row in range(len(spl)):
            for col in range(len(spl[row])):
                if spl[row][col] == '#':
                    self.obstacles.append(Obstacle(row, col))
                elif spl[row][col] == '^' or spl[row][col] == '>' or spl[row][col] == 'v' or spl[row][col] == '<':
                    self.guard = Guard(spl[row][col], row, col)
                    self.visited_coordinates_current.append((self.guard.x, self.guard.y, self.guard.x_dir, self.guard.y_dir))
                    self.visited_coordinates_withoutdir.append((self.guard.x, self.guard.y))

    def move(self):
        self.move_counter += 1
        print('Performing move ' + str(self.move_counter) + '/5670')
        next_guard_position_x, next_guard_position_y = self.guard.peek_move()
        if self.out_of_bounds(next_guard_position_x, next_guard_position_y):
            return True
        if self.in_obstacle(next_guard_position_x, next_guard_position_y):
            self.guard.turn()
            self.visited_coordinates_current.append((self.guard.x, self.guard.y, self.guard.x_dir, self.guard.y_dir))
            return False
        else:
            if self.guard_in_loop(next_guard_position_x, next_guard_position_y):
                return True
            else:
                self.guard.move()
                self.visited_coordinates_current.append(
                    (self.guard.x, self.guard.y, self.guard.x_dir, self.guard.y_dir))
                self.visited_coordinates_withoutdir.append((self.guard.x, self.guard.y))
                return False

    def guard_in_loop(self, next_x, next_y):
        return (next_x, next_y, self.guard.x_dir, self.guard.y_dir) in self.visited_coordinates_current

    def out_of_bounds(self, x, y):
        return x < 0 or x >= self.x_length or y < 0 or y >= self.y_length

    def in_obstacle(self, x, y):
        return (x, y) in zip([obst.x for obst in self.obstacles], [obst.y for obst in self.obstacles])

    def is_guard_in_loop_on_turn_right(self):
        # print('--- Checking if guard is in loop')
        clone_guard = self.guard.clone()
        clone_visited_coordinates_current = [] + self.visited_coordinates_current
        temp_obstacle_x, temp_obstacle_y = clone_guard.peek_move()
        temp_obstacle = Obstacle(temp_obstacle_y, temp_obstacle_x)
        self.obstacles.append(temp_obstacle)
        clone_guard.turn()

        while True:
            next_clone_guard_position_x, next_clone_guard_position_y = clone_guard.peek_move()
            if self.out_of_bounds(next_clone_guard_position_x, next_clone_guard_position_y):
                self.obstacles.remove(temp_obstacle)
                return False
            if self.in_obstacle(next_clone_guard_position_x, next_clone_guard_position_y):
                clone_guard.turn()
            else:
                if (next_clone_guard_position_x, next_clone_guard_position_y, clone_guard.x_dir, clone_guard.y_dir) in clone_visited_coordinates_current:
                    self.obstacles.remove(temp_obstacle)
                    self.extra_obstacle_coords.append((temp_obstacle_x, temp_obstacle_y))
                    return True
                else:
                    clone_guard.move()
                    clone_visited_coordinates_current.append((clone_guard.x, clone_guard.y, clone_guard.x_dir, clone_guard.y_dir))


class Guard:
    def __init__(self, char, y, x):
        self.y = int(y)
        self.x = int(x)
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

    def clone(self):
        res = Guard('^', self.y, self.x)
        res.x_dir = self.x_dir
        res.y_dir = self.y_dir
        return res

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


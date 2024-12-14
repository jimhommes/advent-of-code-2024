from aocd import *
from time import perf_counter
import networkx as nx


class Board:
    def __init__(self, inp):
        self.board = nx.DiGraph()
        self.board.add_node(0)  # start node
        self.end_node_id = 100000
        self.end_node_top_id = 99999
        self.end_node_right_id = 99998
        self.end_node_bottom_id = 99997
        self.end_node_left_id = 99996
        self.board.add_nodes_from([self.end_node_top_id, self.end_node_left_id, self.end_node_bottom_id,
                                   self.end_node_right_id])
        self.matrix_ids = list()
        self.x_length = len(inp[0])
        self.y_length = len(inp)
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
            obstacles_on_guard_path = [(abs(i[1] - self.guard.y), i[2]) for i in self.obstacles if
                                       i[0] == self.guard.x and i[1] > self.guard.y * self.guard.y_dir]
        else:
            obstacles_on_guard_path = [(abs(i[0] - self.guard.x), i[2]) for i in self.obstacles if
                                       i[1] == self.guard.y and i[0] > self.guard.x * self.guard.x_dir]
        obstacles_on_guard_path.sort(key=lambda i: i[0])
        self.board.add_edge(0, obstacles_on_guard_path[0][1], weight=obstacles_on_guard_path[0][0])

        # Add all edges between obstacles
        for obstacle in self.obstacles:
            obstacles_to_right = [(i[0] - obstacle[0], i[2]) for i in self.obstacles if
                                  i[1] == obstacle[1] + 1 and i[0] > obstacle[0]]
            if len(obstacles_to_right) > 0:
                obstacles_to_right.sort(key=lambda i: i[0])
                self.board.add_edge(obstacle[2], obstacles_to_right[0][1], weight=obstacles_to_right[0][0])
            else:
                self.board.add_edge(obstacle[2], self.end_node_right_id, weight=self.x_length - obstacle[0])

            obstacles_to_left = [(obstacle[0] - i[0], i[2]) for i in self.obstacles if
                                 i[1] == obstacle[1] - 1 and i[0] < obstacle[0]]
            if len(obstacles_to_left) > 0:
                obstacles_to_left.sort(key=lambda i: i[0])
                self.board.add_edge(obstacle[2], obstacles_to_left[0][1], weight=obstacles_to_left[0][0])
            else:
                self.board.add_edge(obstacle[2], self.end_node_left_id, weight=obstacle[0])

            obstacles_to_above = [(obstacle[1] - i[1], i[2]) for i in self.obstacles if
                                  i[0] == obstacle[0] + 1 and i[1] < obstacle[1]]
            if len(obstacles_to_above) > 0:
                obstacles_to_above.sort(key=lambda i: i[0])
                self.board.add_edge(obstacle[2], obstacles_to_above[0][1], weight=obstacles_to_above[0][0])
            else:
                self.board.add_edge(obstacle[2], self.end_node_top_id, weight=obstacle[1])

            obstacles_to_bottom = [(i[1] - obstacle[1], i[2]) for i in self.obstacles if
                                   i[0] == obstacle[0] - 1 and i[1] > obstacle[1]]
            if len(obstacles_to_bottom) > 0:
                obstacles_to_bottom.sort(key=lambda i: i[0])
                self.board.add_edge(obstacle[2], obstacles_to_bottom[0][1], weight=obstacles_to_bottom[0][0])
            else:
                self.board.add_edge(obstacle[2], self.end_node_bottom_id, weight=self.y_length - obstacle[1])
        self.board.add_edge(self.end_node_top_id, self.end_node_id, weight=0)
        self.board.add_edge(self.end_node_bottom_id, self.end_node_id, weight=0)
        self.board.add_edge(self.end_node_right_id, self.end_node_id, weight=0)
        self.board.add_edge(self.end_node_left_id, self.end_node_id, weight=0)

    def get_coordinates_between_nodes(self, node_id1, node_id2):
        if node_id1 == 0:
            if self.guard.x_dir == 0 and self.guard.y_dir == -1: # should do for all cases
                node1 = (self.guard.x - 1, self.guard.y, 0)
        else:
            node1 = [nd for nd in self.obstacles if nd[2] == node_id1][0]

        if node_id2 in [self.end_node_top_id, self.end_node_bottom_id, self.end_node_left_id, self.end_node_right_id]:
            if node_id2 == self.end_node_right_id:
                node2 = (self.x_length, node1[1], self.end_node_right_id)
            elif node_id2 == self.end_node_left_id:
                node2 = (-1, node1[1], self.end_node_left_id)
            elif node_id2 == self.end_node_top_id:
                node2 = (node1[0], -1, self.end_node_top_id)
            else:
                # node_id2 == self.end_node_bottom_id:
                node2 = (node1[0], self.y_length, self.end_node_bottom_id)
        else:
            node2 = [nd for nd in self.obstacles if nd[2] == node_id2][0]
        res = []
        if node2[1] == node1[1] + 1 and node2[0] > node1[0]:
            # Node 1 encountered from bottom, turned to the right
            res += [(x, node1[1] + 1) for x in range(node1[0], node2[0] + 1)]
        elif node2[0] == node1[0] - 1 and node2[1] > node1[1]:
            # Node 1 encountered from left, turned to bottom
            res += [(node1[0] - 1, y) for y in range(node1[1], node2[1] + 1)]
        elif node2[1] == node1[1] - 1 and node2[0] < node1[0]:
            # Node 1 encountered from above, turned to left
            res += [(x, node1[1] - 1) for x in reversed(range(node2[0] - 1, node1[0]))]
        else:
            # Node 1 encountered from right, turned to above
            res += [(node1[0] - 1, y) for y in reversed(range(node2[1] - 1, node1[0]))]
        return res


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
shortest_path = nx.shortest_path(board.board, source=0, target=board.end_node_id)
visited_coordinates = []
for i in range(len(shortest_path) - 1):
    visited_coordinates.append(board.get_coordinates_between_nodes(shortest_path[i], shortest_path[i + 1]))
ex1_res = len(set(visited_coordinates))
t1_stop = perf_counter()

print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(ex1_res, part='a', day=6, year=2024)
#
# ex2_res = len(set(board.extra_obstacle_coords))
# print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
# submit(ex2_res, part='b', day=6, year=2024)

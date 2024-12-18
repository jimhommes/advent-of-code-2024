from aocd import *
from time import perf_counter


def rec_find_antinode(lst):
    if len(lst) >= 2:
        curr_el = lst[0]
        for next_el in lst[1:]:
            diff_row = next_el[0] - curr_el[0]
            diff_col = next_el[1] - curr_el[1]
            anti_nodes.append((curr_el[0] - diff_row, curr_el[1] - diff_col))
            anti_nodes.append((next_el[0] + diff_row, next_el[1] + diff_col))
            rec_find_antinode(lst[1:])


t1_start = perf_counter()
lines = get_data(day=8, year=2024).split('\n')
# lines = '............\n........0...\n.....0......\n.......0....\n....0.......\n......A.....\n............\n............\n........A...\n.........A..\n............\n............'.split('\n')
input_rows = len(lines)
input_cols = len(lines[0])
coord_dict = dict()
anti_nodes = []

for row in range(len(lines)):
    for col in range(len(lines[0])):
        el = lines[row][col]
        if el == '.':
            continue
        else:
            if el in coord_dict.keys():
                coord_dict[el].append((row, col))
            else:
                coord_dict[el] = [(row, col)]

for k, v in coord_dict.items():
    rec_find_antinode(v)

ex1_res = len(set([an for an in anti_nodes if 0 <= an[0] < input_rows and 0 <= an[1] < input_cols]))
t1_stop = perf_counter()
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(int(ex1_res), part='a', day=8, year=2024)

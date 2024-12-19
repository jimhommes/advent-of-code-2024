from aocd import *
from time import perf_counter
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

data_input = get_data(day=9, year=2024)
# data_input = '2333133121414131402'
final_list_length = 0
index_dict = {'.': []}
indices = []

t1_start = perf_counter()
for i in range(len(data_input)):
    if i % 2 == 0:
        indices.append(int(i/2))
        amount_of_index = int(data_input[i])

        index_dict[int(i/2)] = list(range(final_list_length, final_list_length + amount_of_index))
        final_list_length += amount_of_index
    else:
        amount_of_empty = int(data_input[i])
        index_dict['.'] += list(range(final_list_length, final_list_length + amount_of_empty))
        final_list_length += amount_of_empty

# print(index_dict)
# print(indices)
# print(final_list_length)
final_list = [False] * final_list_length
# print(final_list)

# Resolve empty '.'
last_placed = final_list_length
for i in index_dict['.']:
    replacements = index_dict[indices[-1]]
    if i < last_placed:
        if len(replacements) == 0:
            index_dict.pop(indices[-1], None)
            indices.pop()
            replacements = index_dict[indices[-1]]
        last_placed = replacements.pop()
        final_list[i] = indices[-1]
    else:
        break

# print(final_list)

# Shove all numbers in front
for k in indices:
    v = index_dict[k]
    for i in v:
        final_list[i] = k
    # print(final_list)

# print(final_list)
final_list = np.array(final_list)
# print(final_list)

ex1_res = np.sum(np.multiply(final_list, np.array(range(final_list.size))).astype(np.float64))
t1_stop = perf_counter()
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(int(ex1_res), part='a', day=9, year=2024)

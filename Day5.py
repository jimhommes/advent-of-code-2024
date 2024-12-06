from aocd import *
from time import perf_counter
import numpy as np

data_input = get_data(day=5, year=2024).split('\n\n')
rules_lines = data_input[0].split('\n')
update_lines = data_input[1].split('\n')
rules = dict()


def update_line_valid(lst):
    vld = True
    vld_i = -1
    inp_i = -1
    for i in range(1, len(lst)):
        page = int(lst[i])
        violations = np.in1d(lst[:i], rules[page])
        if np.any(violations):
            vld = False
            vld_i = np.where(violations)[0][0]
            inp_i = i
            break
    return vld, vld_i, inp_i


def update_line_ordered(lst):
    ordered_lst = list(lst)
    vld, vld_i, inp_i = update_line_valid(ordered_lst)
    while not vld:
        ordered_lst = ordered_lst[:vld_i] + [ordered_lst[inp_i]] + ordered_lst[vld_i:inp_i] + ordered_lst[inp_i+1:]
        vld, vld_i, inp_i = update_line_valid(ordered_lst)
    return ordered_lst


for rule_line in rules_lines:
    spl = rule_line.split('|')
    if int(spl[0]) not in rules.keys():
        rules[int(spl[0])] = [int(spl[1])]
    else:
        rules[int(spl[0])].append(int(spl[1]))

ex1_res = 0
t1_start = perf_counter()
for update_line in update_lines:
    spl = np.array(update_line.split(',')).astype(int)
    if update_line_valid(spl)[0]:
        ex1_res += spl[int((len(spl)-1)/2)]

t1_stop = perf_counter()
print('Part A - Answer: ' + str(ex1_res) + ', calculated in ' + str((t1_stop - t1_start) * 1000) + ' ms')
submit(int(ex1_res), part='a', day=5, year=2024)

ex2_res = 0
t2_start = perf_counter()
for update_line in update_lines:
    spl = np.array(update_line.split(',')).astype(int)
    if not update_line_valid(spl)[0]:
        ordered_update_line = update_line_ordered(spl)
        ex2_res += ordered_update_line[int((len(ordered_update_line) - 1) / 2)]
t2_stop = perf_counter()
print('Part B - Answer: ' + str(ex2_res) + ', calculated in ' + str((t2_stop - t2_start) * 1000) + ' ms')
submit(int(ex2_res), part='b', day=5, year=2024)





